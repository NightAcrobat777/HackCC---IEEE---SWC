import './App.css'

function App() {
  return (
    <div className="app">
      <header>
        <nav>
          <h1>My Site</h1>
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </header>

      <main>
        <section id="home" className="hero">
          <h2>Welcome</h2>
          <p>This is a simple React website.</p>
        </section>

        <section id="about">
          <h2>About</h2>
          <p>Learn more about this project.</p>
        </section>

        <section id="contact">
          <h2>Contact</h2>
          <p>Get in touch with us.</p>
        </section>
      </main>

      <footer>
        <p>&copy; 2024 My Site. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
