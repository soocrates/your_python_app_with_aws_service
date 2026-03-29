import React, { useState } from 'react';

export default function ApplicationModal({ onClose, onSave, initialData }) {
    const [formData, setFormData] = useState(initialData || {
        title: '', company: '', description: '', category: 'Other', status: 'Applied', notes: ''
    });
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await onSave(formData, file);
            onClose();
        } catch (err) {
            alert(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100 }}>
            <div className="glass-panel" style={{ padding: '2rem', width: '100%', maxWidth: '500px', maxHeight: '90vh', overflowY: 'auto' }}>
                <h3>{initialData ? 'Edit Application' : 'New Application'}</h3>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
                    <input name="title" placeholder="Job Title" className="input-field" value={formData.title} onChange={handleChange} required />
                    <input name="company" placeholder="Company" className="input-field" value={formData.company} onChange={handleChange} required />

                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <select name="category" className="input-field" value={formData.category} onChange={handleChange}>
                            <option value="Cloud">Cloud</option>
                            <option value="DevOps">DevOps</option>
                            <option value="Software Engineering">Software Engineering</option>
                            <option value="IT Support">IT Support</option>
                            <option value="Other">Other</option>
                        </select>
                        <select name="status" className="input-field" value={formData.status} onChange={handleChange}>
                            <option value="Applied">Applied</option>
                            <option value="Interviewing">Interviewing</option>
                            <option value="Offer">Offer</option>
                            <option value="Rejected">Rejected</option>
                            <option value="Withdrawn">Withdrawn</option>
                        </select>
                    </div>

                    <textarea name="description" placeholder="Job Description (Optional)" className="input-field" rows="3" value={formData.description || ''} onChange={handleChange}></textarea>
                    <textarea name="notes" placeholder="Notes (Optional)" className="input-field" rows="2" value={formData.notes || ''} onChange={handleChange}></textarea>

                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.875rem' }}>Upload CV</label>
                        <input type="file" className="input-field" onChange={(e) => setFile(e.target.files[0])} accept="application/pdf" />
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
                        <button type="button" className="btn" style={{ background: 'transparent', border: '1px solid var(--border-color)' }} onClick={onClose} disabled={loading}>Cancel</button>
                        <button type="submit" className="btn" disabled={loading}>{loading ? 'Saving...' : 'Save Application'}</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
