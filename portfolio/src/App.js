import React from 'react';
import { Github, Linkedin, Mail, ExternalLink } from 'lucide-react';

const App = () => {
  const projects = [
    {
      title: "Project 1",
      description: "Description of your first project",
      technologies: ["React", "Node.js"],
      githubLink: "https://github.com/Sardean123/project1",
      liveLink: "https://project1.com"
    },
    // Add more projects here
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Dean Casey</h1>
          <p className="text-xl text-gray-600 mb-6">Data Scientist</p>
          <div className="flex space-x-4">
            <a href="https://github.com/Sardean123" className="text-gray-600 hover:text-gray-900">
              <Github size={24} />
            </a>
            <a href="mailto:dscasey02@gmail.com" className="text-gray-600 hover:text-gray-900">
              <Mail size={24} />
            </a>
          </div>
        </div>
      </header>

      {/* Projects */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">My Projects</h2>
          <div className="grid gap-8 md:grid-cols-2">
            {projects.map((project, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{project.title}</h3>
                <p className="text-gray-600 mb-4">{project.description}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {project.technologies.map((tech, techIndex) => (
                    <span key={techIndex} className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm">
                      {tech}
                    </span>
                  ))}
                </div>
                <div className="flex space-x-4">
                  <a href={project.githubLink} className="flex items-center text-gray-600 hover:text-gray-900">
                    <Github size={20} className="mr-1" />
                    Code
                  </a>
                  <a href={project.liveLink} className="flex items-center text-gray-600 hover:text-gray-900">
                    <ExternalLink size={20} className="mr-1" />
                    Live Demo
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Skills */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Skills</h2>
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Frontend</h3>
              <ul className="text-gray-600">
                <li>React</li>
                <li>JavaScript</li>
                <li>HTML/CSS</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Backend</h3>
              <ul className="text-gray-600">
                <li>Node.js</li>
                <li>Express</li>
                <li>MongoDB</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Tools</h3>
              <ul className="text-gray-600">
                <li>Git</li>
                <li>VS Code</li>
                <li>Docker</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Contact */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">Get In Touch</h2>
          <p className="text-lg text-gray-600 mb-6">
            I'm currently open to new opportunities. Feel free to reach out!
          </p>
          <a href="mailto:your.email@example.com" 
             className="inline-flex items-center px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800">
            <Mail size={20} className="mr-2" />
            Contact Me
          </a>
        </div>
      </section>

      <footer className="py-8 bg-white">
        <div className="max-w-4xl mx-auto px-4 text-center text-gray-600">
          <p>© {new Date().getFullYear()} Dean Casey</p>
        </div>
      </footer>
    </div>
  );
};

export default App;