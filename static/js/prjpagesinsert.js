// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');

    // Get the project ID from the URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const projectId = urlParams.get('project');
    console.log('Project ID:', projectId);

    // Find the project data based on the project ID
    const project = projects.find(p => p.id === projectId);
    console.log('Project Data:', project);

    // If the project is not found, handle the error
    if (!project) {
        document.getElementById('project-header').innerHTML = '<h1>Project not found</h1>';
        return;
    }

    // Set project header content
    const projectHeader = document.getElementById('project-header');
    projectHeader.innerHTML = `
        <h1>${project.name}</h1>
        <div class="tags">
            ${project.tags.map(tag => `<span class="badge badge-pill badge-primary">${tag}</span>`).join(' ')}
        </div>
        <p class="overview">${project.overview}</p>
        <a href="${project.github}" class="btn btn-dark btn-github" target="_blank">
            <i class="fab fa-github"></i> View on GitHub
        </a>
        <a href="${project.linkedin}" class="btn btn-primary btn-linkedin" target="_blank">
            <i class="fab fa-linkedin"></i> Connect on LinkedIn
        </a>
    `;

    // Set carousel content
    const carouselContainer = document.getElementById('carouselExampleIndicators');
    carouselContainer.innerHTML = `
        <ol class="carousel-indicators">
            ${project.images.map((_, index) => `<li data-target="#carouselExampleIndicators" data-slide-to="${index}" class="${index === 0 ? 'active' : ''}"></li>`).join('')}
        </ol>
        <div class="carousel-inner">
            ${project.images.map((image, index) => `
                <div class="carousel-item ${index === 0 ? 'active' : ''}">
                    <img src="${image}" class="d-block w-100" alt="...">
                </div>
            `).join('')}
        </div>
        <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
    `;

    // Set readme content
    const readmeContainer = document.getElementById('readme-container');
    readmeContainer.innerHTML = `
        <h2>Readme File</h2>
        <pre>${project.readme}</pre>
    `;

    // Set video content
    const projectVideo = document.getElementById('project-video');
    projectVideo.src = project.video;
});
