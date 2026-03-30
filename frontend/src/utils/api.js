const API_URL = 'http://localhost:8000';

export const login = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString()
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
};

export const register = async (email, password) => {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Registration failed');
    }
    return response.json();
};

export const getApplications = async (token) => {
    const response = await fetch(`${API_URL}/applications/`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to fetch applications');
    return response.json();
};

export const createApplication = async (token, application) => {
    const response = await fetch(`${API_URL}/applications/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(application)
    });
    if (!response.ok) throw new Error('Failed to create application');
    return response.json();
};

export const updateApplication = async (token, id, application) => {
    const response = await fetch(`${API_URL}/applications/${id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(application)
    });
    if (!response.ok) throw new Error('Failed to update application');
    return response.json();
};

export const uploadCV = async (token, appId, file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/applications/${appId}/cv/upload`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        },
        body: formData
    });

    if (!response.ok) throw new Error("Failed to upload CV");
    return response.json();
};

export const getDownloadUrl = async (token, appId) => {
    const response = await fetch(`${API_URL}/applications/${appId}/cv/download-url`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to get download URL');
    return response.json();
};
