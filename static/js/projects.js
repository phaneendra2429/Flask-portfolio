document.addEventListener('DOMContentLoaded', function () {
  const data = {
    "gen-ai": [
      {
        "title": "Text Generation with GPT-3",
        "description": "Using OpenAI's GPT-3 for generating human-like text for various applications.",
        "image": "https://via.placeholder.com/150",
        "tags": ["Generative AI", "NLP", "GPT-3"],
        "link": "#"
      }
    ],
    "ml-projects": [
      {
        "title": 'Melanoma Skin Cancer Detection',
        "description": '',
        "tags": ['Deep Learning', 'Neural Networks'],
        "image": '../projects/ML Projects/image2.png',
        "link": "project.html?project=project2"

      }, 
    ],

      "sql": [
      {
        "title": 'SweepShift: Refining Layoffs Data for Analysis',
        "description": '',
        "tags": ['Data cleaning', 'Data Analysis'],
        "image": '../projects/SQL/image.png',
        "link": 'project.html?project=project2'
      }
    ],

    "excel": [
      {
        "title": 'Coffee Shop Sales',
        "description": '',
        "tags": ['Dashboard', 'Data Analysis'],
        "image": '../projects/Excel/image.png',
        "link": 'project.html?project=project2'
      }
    ],

    "tableau": [
      {
        "title": 'SweepShift: Refining Layoffs Data for Analysis',
        "description": '',
        "tags": ['Data cleaning', 'Data Analysis'],
        "image": 'D:/3. My_Projects/Porfolio/portfolio_website/projects/SQL/image.png',
        "link": 'project.html?project=project2'
      }
    ],

    "aws": [
      {
        "title": 'SweepShift: Refining Layoffs Data for Analysis',
        "description": '',
        "tags": ['Data cleaning', 'Data Analysis'],
        "image": '../projects/cloud/image.png',
        "link": 'project.html?project=project2'
      }
    ]
  };

  renderProjects('gen-ai', data['gen-ai']);
  renderProjects('ml-projects', data['ml-projects']);
  renderProjects('sql', data['sql']);
  renderProjects('excel', data['excel']);
  // renderProjects('tableau', data['tableau']);
  renderProjects('aws', data['aws']);

});

function renderProjects(tabId, projects) {
  const tabContent = document.getElementById(tabId);

  projects.forEach(project => {
    const projectCard = document.createElement('div');
    projectCard.className = 'project-card';

    projectCard.innerHTML = `
      <img src="${project.image}" alt="Project Image">
      <h3>${project.title}</h3>
      <p>${project.description}</p>
      <div class="tags">${project.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}</div>
      <a href="${project.link}" class="btn">View Project</a>
    `;

    tabContent.appendChild(projectCard);
  });
}

function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tab-link");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "flex";
  evt.currentTarget.className += " active";
}
