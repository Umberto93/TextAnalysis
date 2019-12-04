class DOM {
    static render(element, container) {
        container.innerHTML = element;
    }
}

class Router {
    constructor(routes) {
        this.routes = routes;
        this.activeComponent = new this.routes[location.hash]();
        this.app = app;
        this.init();
    }

    init() {
        window.addEventListener('hashchange', () => {
            const router = document.getElementById('router');

            if (router) {
                this.activeComponent = new this.routes[location.hash]();
                router.removeChild(router.firstElementChild);
                router.insertAdjacentHTML('afterbegin', this.activeComponent.render());
                eel.py_request(location.hash)(this.activeComponent.getData);
            }
        });

        eel.py_request(location.hash)(this.activeComponent.getData);
    }

    getActiveComponent() {
        return this.activeComponent;
    }
}

class Component {
    constructor() {}
    getData() {}
    render() {}
}

class App extends Component {
    constructor() {
        super();
        this.router = new Router({
            '': Articles,
            '#articles': Articles,
            '#classification': Pippo
        });
    }

    render() {
        return `
            <main id="router">
                ${new Sidebar().render()}
                ${this.router.getActiveComponent().render()}
            </main>
        `;
    }
}

class Sidebar extends Component {
    constructor() {
        super();
    }

    render() {
        return `
            <aside class="sidebar">
                <h1 class="logo">TextAnalysis</h1>
                <nav class="nav">
                    <h2>Categorie</h2>
                    <ul class="nav-menu">
                        <li><a href="#articles">Articles</a></li>
                        <li><a href="#classification">Text Classification</a></li>
                        <li><a href="#query">Query Builder</a></li>
                        <li><a href="#about">About Us</a></li>
                    </ul>
                </nav>
            </aside>
        `;
    }
}

class Filter extends Component {
    constructor(options) {
        super();
        this.options = options;
    }

    render() {
        return `
            <select>
                ${this.options.map((option) => {
                    return `
                        <option>${option}</option>
                    `;
                }).join('')}
            </select>
        `;
    }
}

class Search extends Component {
    constructor() {
        super();
    }

    render() {
        return `
            <div class="search">
                <input type="text" placeholder="Inserisci le keywords separate da una ','">
            </div>
        `;
    }
}

class Articles extends Component {
    constructor() {
        super();
        this.data = null;
    }

    getData(data) {
        console.log(data);
        this.data = data;
    }

    render() {
        return `
            <section class="articles">
                <header>
                    <h2>Categoria</h2>
                    ${new Search().render()}
                    ${this.data}
                </header>

            </section>
        `;
    }
}

class Pippo extends Component {
    constructor() {
        super();
    }

    render() {
        return `
            <h1>Pippo</h1>
        `;
    }
}

DOM.render(new App().render(), document.getElementById('app'))