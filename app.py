from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuração
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eln.db'
app.config['SECRET_KEY'] = 'sua-chave-secreta-mude-em-producao'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file
app.config['UPLOAD_FOLDER'] = 'uploads'

# Criar pasta de upload se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Modelos do banco de dados
class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    experiments = db.relationship('Experiment', backref='sample', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Sample {self.name}>'

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    attachments = db.relationship('Attachment', backref='experiment', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Experiment {self.title}>'

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Attachment {self.original_filename}>'

# Criar as tabelas
with app.app_context():
    db.create_all()

# Rotas
@app.route('/')
def index():
    samples = Sample.query.all()
    return render_template('index.html', samples=samples)

@app.route('/sample/new', methods=['GET', 'POST'])
def new_sample():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            return jsonify({'error': 'Nome da amostra é obrigatório'}), 400
        
        sample = Sample(name=name, description=description)
        db.session.add(sample)
        db.session.commit()
        
        return redirect(url_for('view_sample', sample_id=sample.id))
    
    return render_template('new_sample.html')

@app.route('/sample/<int:sample_id>')
def view_sample(sample_id):
    sample = Sample.query.get_or_404(sample_id)
    return render_template('view_sample.html', sample=sample)

@app.route('/sample/<int:sample_id>/experiment/new', methods=['GET', 'POST'])
def new_experiment(sample_id):
    sample = Sample.query.get_or_404(sample_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        notes = request.form.get('notes')
        
        if not title:
            return jsonify({'error': 'Título do experimento é obrigatório'}), 400
        
        experiment = Experiment(sample_id=sample_id, title=title, description=description, notes=notes)
        
        # Processar arquivo se enviado
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                file_type = filename.split('.')[-1] if '.' in filename else 'unknown'
                attachment = Attachment(
                    filename=filename,
                    original_filename=request.form.get('file', file.filename),
                    file_type=file_type
                )
                experiment.attachments.append(attachment)
        
        db.session.add(experiment)
        db.session.commit()
        
        return redirect(url_for('view_sample', sample_id=sample_id))
    
    return render_template('new_experiment.html', sample=sample)

@app.route('/sample/<int:sample_id>/delete', methods=['POST'])
def delete_sample(sample_id):
    sample = Sample.query.get_or_404(sample_id)
    db.session.delete(sample)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/experiment/<int:experiment_id>/delete', methods=['POST'])
def delete_experiment(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)
    sample_id = experiment.sample_id
    db.session.delete(experiment)
    db.session.commit()
    return redirect(url_for('view_sample', sample_id=sample_id))

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        # Buscar em amostras
        sample_results = Sample.query.filter(
            (Sample.name.ilike(f'%{query}%')) | (Sample.description.ilike(f'%{query}%'))
        ).all()
        
        # Buscar em experimentos
        experiment_results = Experiment.query.filter(
            (Experiment.title.ilike(f'%{query}%')) | (Experiment.description.ilike(f'%{query}%'))
        ).all()
        
        results = {
            'samples': sample_results,
            'experiments': experiment_results
        }
    
    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
