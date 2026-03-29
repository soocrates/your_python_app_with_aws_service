import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getApplications, createApplication, updateApplication, uploadCV, getDownloadUrl } from '../utils/api';
import ApplicationModal from '../components/ApplicationModal';

export default function Dashboard() {
    const [applications, setApplications] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingApp, setEditingApp] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const token = localStorage.getItem('ats_token');

    useEffect(() => {
        if (!token) {
            navigate('/login');
            return;
        }
        fetchData();
    }, [token, navigate]);

    const fetchData = async () => {
        try {
            setLoading(true);
            const data = await getApplications(token);
            setApplications(data);
        } catch (err) {
            setError('Failed to load applications. Please login again.');
            localStorage.removeItem('ats_token');
            navigate('/login');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('ats_token');
        navigate('/login');
    };

    const handleSaveApp = async (formData, file) => {
        let appId;
        if (editingApp) {
            await updateApplication(token, editingApp.id, formData);
            appId = editingApp.id;
        } else {
            const newApp = await createApplication(token, formData);
            appId = newApp.id;
        }

        if (file) {
            await uploadCV(token, appId, file);
        }
        await fetchData();
    };

    const handleDownloadCV = async (appId) => {
        try {
            const { url } = await getDownloadUrl(token, appId);
            window.open(url, '_blank');
        } catch (err) {
            alert('Could not download CV: ' + err.message);
        }
    };

    return (
        <div>
            <nav className="nav">
                <div className="nav-brand">✨ ATS-lite</div>
                <button className="btn" onClick={handleLogout} style={{ background: 'rgba(255,255,255,0.1)' }}>Logout</button>
            </nav>
            <div className="container">

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                    <h2>My Applications</h2>
                    <button className="btn" onClick={() => { setEditingApp(null); setIsModalOpen(true); }}>
                        + New Application
                    </button>
                </div>

                {loading ? (
                    <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '4rem' }}>Loading...</div>
                ) : applications.length === 0 ? (
                    <div className="glass-panel" style={{ padding: '4rem 2rem', textAlign: 'center' }}>
                        <h3 style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>No applications yet</h3>
                        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Track your first job application today!</p>
                        <button className="btn" onClick={() => { setEditingApp(null); setIsModalOpen(true); }}>Get Started</button>
                    </div>
                ) : (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
                        {applications.map(app => (
                            <div key={app.id} className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                                    <div>
                                        <h3 style={{ fontSize: '1.125rem', marginBottom: '0.25rem' }}>{app.title}</h3>
                                        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{app.company}</p>
                                    </div>
                                    <span className={`badge badge-${app.status.toLowerCase()}`}>{app.status}</span>
                                </div>

                                <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1.5rem', display: 'flex', gap: '1rem' }}>
                                    <span>{app.category}</span>
                                    <span>•</span>
                                    <span>{new Date(app.date_applied).toLocaleDateString()}</span>
                                </div>

                                <div style={{ marginTop: 'auto', display: 'flex', gap: '0.5rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
                                    <button className="btn" style={{ flex: 1, background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }} onClick={() => { setEditingApp(app); setIsModalOpen(true); }}>
                                        Edit
                                    </button>
                                    {app.cv_s3_key && (
                                        <button className="btn" style={{ flex: 1, background: 'rgba(16, 185, 129, 0.2)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.3)' }} onClick={() => handleDownloadCV(app.id)}>
                                            CV
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {isModalOpen && (
                <ApplicationModal
                    initialData={editingApp}
                    onClose={() => setIsModalOpen(false)}
                    onSave={handleSaveApp}
                />
            )}
        </div>
    );
}
