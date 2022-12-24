let subtaskId = 0

const createSubtask = () => {
    const subtaskDiv = document.getElementById('subtasks')
    const subtaskInput = document.createElement('input')
    subtaskInput.type = 'text'
    subtaskInput.name = 'subtask'
    subtaskInput.className = 'form-control'

    const inputGroupDiv = document.createElement('div')
    inputGroupDiv.className = 'input-group mb-3'
    subtaskId += 1
    inputGroupDiv.id = subtaskId

    const inputGroupAppendDiv = document.createElement('div')
    inputGroupAppendDiv.className = 'input-group-append'

    const deleteSubtaskBtn = document.createElement('button')
    deleteSubtaskBtn.className = 'btn btn-danger rounded-0'
    deleteSubtaskBtn.type = 'button'
    deleteSubtaskBtn.innerText = 'Delete'
    deleteSubtaskBtn.onclick = () => deleteSubtask(inputGroupDiv.id)
    
    inputGroupDiv.append(subtaskInput)
    inputGroupDiv.appendChild(inputGroupAppendDiv)
    inputGroupAppendDiv.appendChild(deleteSubtaskBtn)
    subtaskDiv.appendChild(inputGroupDiv)
}

const deleteSubtask = (id) => {
    const subtask = document.getElementById(id)
    const parentDiv = subtask.parentNode
    parentDiv.removeChild(subtask)
}

const deleteAllSubtasks = () => {
    const subtaskDiv = document.getElementById('subtasks')
    while (subtaskDiv.firstChild) {
        subtaskDiv.removeChild(subtaskDiv.firstChild)
    }
}

const addSubtaskBtn = document.getElementById('addSubtask')
addSubtaskBtn.addEventListener('click', () => {createSubtask()})