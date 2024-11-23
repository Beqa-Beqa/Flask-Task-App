const handleLogout = async (e) => {
    // Get logout url from data- attributes of element.
    const logoutUrl = e.target.dataset.logoutUrl;
    const response = await fetch(logoutUrl, {method: 'POST'});

    // If response was to redirect us, follow the link
    // (if the request is made without javascript i.e. without AJAX or fetch
    // The browser does not follow the redirect link in case of 302 status code,
    // So we have to do that manually.
    // If no javascript was involved in request, browser would do that for us.)
    if (response.redirected) window.location.href = response.url;
}


const handleTaskDelete = async (e, tid) => {
    const taskDelUrl = e.target.dataset.deltaskUrl;
    const response = await fetch(taskDelUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tid })
    });

    if (response.redirected) window.location.href = response.url;
}


let visibleTaskId = undefined;
const editTaskModalVisibility = (show, tid) => {
    const taskModal = document.getElementById('task-edit-modal');
    if (show === 'show') {
        taskModal.classList.remove('d-none');
        visibleTaskId = tid;
        console.log(visibleTaskId);
    }
    else if (show === 'hide') {
        taskModal.classList.add('d-none');
        visibleTaskId = undefined;
        console.log(visibleTaskId);
        
    }
}


const handleTaskEdit = async (e) => {
    e.preventDefault();
    
    const newTitle = document.getElementById('edit-task-title').value.trim();
    const newDescription = document.getElementById('edit-task-description').value.trim();
    const editTaskUrl = e.target.dataset.edittaskUrl;
    const tid = visibleTaskId;

    const response = await fetch(editTaskUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tid, newTitle, newDescription })
    })

    if (response.redirected) {
        window.location.href = response.url;
    }

    editTaskModalVisibility('hide', visibleTaskId);
}