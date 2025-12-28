const API_BASE = '/api';

class TaskAPI {
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Request failed' }));
            throw new Error(error.error || 'Request failed');
        }
        return response.json();
    }

    async getAllTasks() {
        const response = await fetch(`${API_BASE}/tasks`);
        return this.handleResponse(response);
    }

    async getTask(id) {
        const response = await fetch(`${API_BASE}/tasks/${id}`);
        return this.handleResponse(response);
    }

    async createTask(description) {
        const response = await fetch(`${API_BASE}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description }),
        });
        return this.handleResponse(response);
    }

    async updateTask(id, updates) {
        const response = await fetch(`${API_BASE}/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updates),
        });
        return this.handleResponse(response);
    }

    async deleteTask(id) {
        const response = await fetch(`${API_BASE}/tasks/${id}`, {
            method: 'DELETE',
        });
        return this.handleResponse(response);
    }

    async filterByTag(tag) {
        const response = await fetch(`${API_BASE}/tasks/filter/tag/${encodeURIComponent(tag)}`);
        return this.handleResponse(response);
    }

    async filterByStatus(status) {
        const response = await fetch(`${API_BASE}/tasks/filter/status/${encodeURIComponent(status)}`);
        return this.handleResponse(response);
    }

    async searchTasks(query) {
        const response = await fetch(`${API_BASE}/tasks/search?q=${encodeURIComponent(query)}`);
        return this.handleResponse(response);
    }

    async saveData() {
        const response = await fetch(`${API_BASE}/save`, {
            method: 'POST',
        });
        return this.handleResponse(response);
    }
}

const api = new TaskAPI();
