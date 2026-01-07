let currentFilter = 'all';
let currentSearchQuery = '';
let currentTask = null;

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function isOverdue(dueDateString) {
    if (!dueDateString) return false;
    const dueDate = new Date(dueDateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return dueDate < today;
}

function createTaskCard(task) {
    const card = document.createElement('div');
    card.className = `task-card status-${task.status.toLowerCase()}`;
    card.dataset.taskId = task.id;

    const header = document.createElement('div');
    header.className = 'task-header';

    const description = document.createElement('div');
    description.className = 'task-description';
    description.textContent = task.description;

    const headerRight = document.createElement('div');
    headerRight.className = 'task-header-right';

    const taskId = document.createElement('span');
    taskId.className = 'task-id';
    taskId.textContent = `#${task.id}`;

    const taskDate = document.createElement('span');
    taskDate.className = 'task-date';
    taskDate.textContent = task.date_created;

    headerRight.appendChild(taskId);
    headerRight.appendChild(taskDate);

    header.appendChild(description);
    header.appendChild(headerRight);

    const meta = document.createElement('div');
    meta.className = 'task-meta';

    const statusLabel = document.createElement('span');
    statusLabel.className = 'status-label';
    statusLabel.textContent = 'Status: ';
    meta.appendChild(statusLabel);

    const statusBadge = document.createElement('span');
    statusBadge.className = `status-badge ${task.status.toLowerCase()}`;
    statusBadge.textContent = task.status;
    meta.appendChild(statusBadge);

    if (task.priority === 'HIGH') {
        const priorityBadge = document.createElement('span');
        priorityBadge.className = 'priority-badge';
        priorityBadge.textContent = 'HIGH PRIORITY';
        meta.appendChild(priorityBadge);
    }

    if (task.tag) {
        const tagLabel = document.createElement('span');
        tagLabel.className = 'status-label';
        tagLabel.textContent = 'Tag: ';
        meta.appendChild(tagLabel);

        const tagBadge = document.createElement('span');
        tagBadge.className = 'tag-badge';
        tagBadge.textContent = task.tag;
        meta.appendChild(tagBadge);
    }

    if (task.date_due) {
        const dueDate = document.createElement('span');
        dueDate.className = 'due-date';
        if (isOverdue(task.date_due)) {
            dueDate.classList.add('overdue');
        }
        dueDate.textContent = `Due: ${task.date_due}`;
        meta.appendChild(dueDate);
    }

    if (task.note) {
        const noteIndicator = document.createElement('span');
        noteIndicator.textContent = '📝 Has note';
        noteIndicator.style.color = '#666';
        noteIndicator.style.fontSize = '13px';
        meta.appendChild(noteIndicator);
    }

    const actions = document.createElement('div');
    actions.className = 'task-actions';

    if (task.status !== 'Done') {
        if (task.status !== 'Doing') {
            const startBtn = document.createElement('button');
            startBtn.className = 'task-action-btn';
            startBtn.textContent = 'Start';
            startBtn.onclick = (e) => {
                e.stopPropagation();
                updateTaskStatus(task.id, 'Doing');
            };
            actions.appendChild(startBtn);
        }

        const doneBtn = document.createElement('button');
        doneBtn.className = 'task-action-btn';
        doneBtn.textContent = 'Complete';
        doneBtn.onclick = (e) => {
            e.stopPropagation();
            updateTaskStatus(task.id, 'Done');
        };
        actions.appendChild(doneBtn);
    }

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'task-action-btn delete';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = (e) => {
        e.stopPropagation();
        deleteTask(task.id);
    };
    actions.appendChild(deleteBtn);

    const bottomRow = document.createElement('div');
    bottomRow.className = 'task-bottom-row';
    bottomRow.appendChild(meta);
    bottomRow.appendChild(actions);

    card.appendChild(header);
    card.appendChild(bottomRow);

    card.onclick = () => showTaskDetail(task);

    return card;
}

function renderTasks(tasks) {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    if (!tasks || tasks.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = `
            <h3>No tasks found</h3>
            <p>Add a new task to get started!</p>
        `;
        taskList.appendChild(emptyState);
        return;
    }

    tasks.forEach(task => {
        taskList.appendChild(createTaskCard(task));
    });
}

function filterTasks(tasks) {
    let filtered = tasks;

    if (currentFilter !== 'all') {
        filtered = filtered.filter(task => {
            if (currentFilter === 'incomplete') {
                return task.status === 'Incomplete';
            } else if (currentFilter === 'doing') {
                return task.status === 'Doing';
            } else if (currentFilter === 'done') {
                return task.status === 'Done';
            }
            return true;
        });
    }

    if (currentSearchQuery) {
        const query = currentSearchQuery.toLowerCase();
        filtered = filtered.filter(task =>
            task.description.toLowerCase().includes(query)
        );
    }

    return filtered;
}

async function loadTasks() {
    try {
        const data = await api.getAllTasks();
        const filtered = filterTasks(data.tasks);
        renderTasks(filtered);
    } catch (error) {
        console.error('Error loading tasks:', error);
        document.getElementById('taskList').innerHTML = `
            <div class="empty-state">
                <h3>Error loading tasks</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
}

async function addTask() {
    const input = document.getElementById('taskInput');
    const description = input.value.trim();

    if (!description) {
        alert('Please enter a task description');
        return;
    }

    try {
        await api.createTask(description);
        input.value = '';
        await loadTasks();
    } catch (error) {
        console.error('Error adding task:', error);
        alert('Error adding task: ' + error.message);
    }
}

async function updateTaskStatus(taskId, status) {
    try {
        await api.updateTask(taskId, { status });
        await loadTasks();
    } catch (error) {
        console.error('Error updating task:', error);
        alert('Error updating task: ' + error.message);
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        await api.deleteTask(taskId);
        await loadTasks();
    } catch (error) {
        console.error('Error deleting task:', error);
        alert('Error deleting task: ' + error.message);
    }
}

function showTaskDetail(task) {
    currentTask = task;

    document.getElementById('detailDescription').textContent = task.description;
    document.getElementById('detailStatus').textContent = task.status;
    document.getElementById('detailPriority').textContent = task.priority;
    document.getElementById('detailCreated').textContent = task.date_created;

    const dueDateSection = document.getElementById('dueDateSection');
    if (task.date_due) {
        document.getElementById('detailDue').textContent = task.date_due;
        dueDateSection.style.display = 'block';
    } else {
        dueDateSection.style.display = 'none';
    }

    const tagSection = document.getElementById('tagSection');
    if (task.tag) {
        document.getElementById('detailTag').textContent = task.tag;
        tagSection.style.display = 'block';
    } else {
        tagSection.style.display = 'none';
    }

    const noteSection = document.getElementById('noteSection');
    if (task.note) {
        document.getElementById('detailNote').textContent = task.note;
        noteSection.style.display = 'block';
    } else {
        noteSection.style.display = 'none';
    }

    document.getElementById('taskModal').classList.add('show');
}

function closeTaskModal(keepCurrentTask = false) {
    document.getElementById('taskModal').classList.remove('show');
    if (!keepCurrentTask) {
        currentTask = null;
    }
}

function showEditModal() {
    if (!currentTask) return;

    document.getElementById('editStatus').value = currentTask.status;
    document.getElementById('editPriority').value = currentTask.priority;
    document.getElementById('editDueDate').value = currentTask.date_due || '';
    document.getElementById('editTag').value = currentTask.tag || '';
    document.getElementById('editNote').value = currentTask.note || '';

    closeTaskModal(true); // Keep currentTask for edit modal
    document.getElementById('editModal').classList.add('show');
}

function closeEditModal() {
    document.getElementById('editModal').classList.remove('show');
    currentTask = null;
}

async function saveEdit() {
    if (!currentTask) return;

    const updates = {
        status: document.getElementById('editStatus').value,
        priority: document.getElementById('editPriority').value,
        date_due: document.getElementById('editDueDate').value || null,
        tag: document.getElementById('editTag').value || null,
        note: document.getElementById('editNote').value || null,
    };

    try {
        await api.updateTask(currentTask.id, updates);
        closeEditModal();
        await loadTasks();
    } catch (error) {
        console.error('Error updating task:', error);
        alert('Error updating task: ' + error.message);
    }
}

function setFilter(filter) {
    currentFilter = filter;

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    document.querySelector(`[data-filter="${filter}"]`).classList.add('active');

    loadTasks();
}

document.addEventListener('DOMContentLoaded', () => {
    loadTasks();

    document.getElementById('addTaskBtn').addEventListener('click', addTask);

    document.getElementById('taskInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            setFilter(btn.dataset.filter);
        });
    });

    document.getElementById('searchInput').addEventListener('input', (e) => {
        currentSearchQuery = e.target.value;
        loadTasks();
    });

    document.querySelector('.close').addEventListener('click', closeTaskModal);
    document.getElementById('closeModalBtn').addEventListener('click', closeTaskModal);
    document.getElementById('editTaskBtn').addEventListener('click', showEditModal);

    document.querySelector('.edit-close').addEventListener('click', closeEditModal);
    document.getElementById('cancelEditBtn').addEventListener('click', closeEditModal);
    document.getElementById('saveEditBtn').addEventListener('click', saveEdit);

    window.addEventListener('click', (e) => {
        const taskModal = document.getElementById('taskModal');
        const editModal = document.getElementById('editModal');
        if (e.target === taskModal) {
            closeTaskModal();
        }
        if (e.target === editModal) {
            closeEditModal();
        }
    });
});
