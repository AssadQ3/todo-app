function loadTasks() {
    fetch('/api/tasks')
        .then(res => res.json())
        .then(tasks => {
            const taskList = document.getElementById('taskList');
            taskList.innerHTML = '';
            tasks.forEach(task => {
                const li = document.createElement('li');
                li.className = 'task-item' + (task.completed ? ' completed' : '');
                li.innerHTML = `
                    <span class="task-title" onclick="toggleTask(${task.id})">${task.title}</span>
                    <div class="task-buttons">
                        <button class="complete-btn" onclick="toggleTask(${task.id})">✓</button>
                        <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
                    </div>
                `;
                taskList.appendChild(li);
            });
        });
}

function addTask() {
    const input = document.getElementById('taskInput');
    const title = input.value.trim();
    
    if (title === '') {
        alert('Please enter a task!');
        return;
    }
    
    fetch('/api/tasks', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title: title})
    })
    .then(res => res.json())
    .then(task => {
        input.value = '';
        loadTasks();
    });
}

function deleteTask(id) {
    fetch(`/api/tasks/${id}`, {method: 'DELETE'})
        .then(res => res.json())
        .then(data => loadTasks());
}

function toggleTask(id) {
    fetch(`/api/tasks/${id}`, {method: 'PUT'})
        .then(res => res.json())
        .then(data => loadTasks());
}

loadTasks();