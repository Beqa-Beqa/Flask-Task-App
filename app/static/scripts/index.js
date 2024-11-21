const handleLogout = async (e) => {
    // Get logout url from data- attributes of element.
    const logoutUrl = e.target.dataset.logoutUrl;
    const response = await fetch(logoutUrl);

    // If response was to redirect us, follow the link
    // (if the request is made without javascript i.e. without AJAX or fetch
    // The browser does not follow the redirect link in case of 302 status code,
    // So we have to do that manually.
    // If no javascript was involved in request, browser would do that for us.)
    if (response.redirected) window.location.href = response.url;
}