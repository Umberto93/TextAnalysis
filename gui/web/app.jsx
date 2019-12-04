class App extends React.Component {
    constructor() {
        super();

        this.routes = {
            '*': <NotFound />,
            '': <Articles />,
            '#articles': <Articles />,
            '#classification': <Classification />
        };

        this.state = {
            activeComponent: this.routes[location.hash] || this.routes['*']
        };

        this._init();
    }

    _init() {
        this.setActiveRoute = this.setActiveRoute.bind(this);

        window.addEventListener('hashchange', this.setActiveRoute);
    }

    setActiveRoute() {
        this.setState({
            activeComponent: this.routes[location.hash] || this.routes['*']
        });
    }

    render() {
        return (
            <main>
                <Sidebar />
                {this.state.activeComponent}
            </main>
        );
    }
}

class Sidebar extends React.Component {
    constructor() {
        super();
    }

    isActive(hash) {
        return location.hash === hash;
    }

    render() {
        return (
            <aside class="sidebar">
                <div class="logo">
                    <h1>Kency</h1>
                </div>
                <nav class="nav">
                    <h2 className="title">Categorie</h2>
                    <ul className="nav-menu">
                        <li className={(this.isActive('') || this.isActive('#articles')) && 'active'}>
                            <a href="#articles">
                                <i class="fa fa-file-text" aria-hidden="true"></i>
                                Articles
                            </a>
                        </li>
                        <li className={this.isActive('#classification') && 'active'}>
                            <a href="#classification">
                                <i class="fa fa-cogs" aria-hidden="true"></i>
                                Text Classification
                            </a>
                        </li>
                        <li className={this.isActive('#query') && 'active'}>
                            <a href="#query">
                                <i class="fa fa-database" aria-hidden="true"></i>
                                Query Builder
                            </a>
                        </li>
                        <li className={this.isActive('#about') && 'active'}>
                            <a href="#about">
                                <i class="fa fa-users" aria-hidden="true"></i>
                                About Us
                            </a>
                        </li>
                    </ul>
                </nav>
            </aside>
        );
    }
}

class Articles extends React.Component {
    constructor() {
        super();

        this.state = {
            categories: [],
            documents: [],
            docs: [],
            catIndex: 0
        };

        this._init();
    }

    _init() {
        this.getCategories = this.getCategories.bind(this);
        this.getDocuments = this.getDocuments.bind(this);
        this.setCategory = this.setCategory.bind(this);

        eel.py_request('/categories')(this.getCategories);
    }

    setCategory(index) {
        this.setState({
            catIndex: index,
            documents: []
        });

        this.getDocumentsByCategory(this.state.categories[index].id);
    }

    getCategories(categories) {
        this.setState({
            categories: categories
        });

        this.getDocumentsByCategory(this.state.categories[0].id);
    }

    getDocuments(docs) {
        console.log(docs[0]);
        this.setState({
            documents: docs
        });
    }

    getDocumentsByCategory(category) {
        eel.py_request('/articles', {
            has_category: category
        })(this.getDocuments);
    }

    searchKeywords() {
        
    }

    render() {
        return (
            <section class="documents">
                <header>
                    <Selection options={this.state.categories} setCategory={this.setCategory} />
                    <div className="search" contenteditable="true"></div>
                </header>
                {this.state.documents.length === 0 ?
                    <Loading /> :
                    this.state.documents.map(doc => {
                        return (
                            <article class="document">
                                <h2>{doc.entity_name}</h2>
                                <p>{doc.has_content.slice(0, 249) + '...'}</p>
                            </article>
                        );
                    })}
            </section>
        );
    }
}

class Classification extends React.Component {
    constructor() {
        super();
    }

    render() {
        return (
            <section>
                CIAOOOO
            </section>
        );
    }
}

class NotFound extends React.Component {
    constructor() {
        super();
    }

    render() {
        return (
            <section class="not-found">
                <i class="fa fa-meh-o" aria-hidden="true"></i>
                <h2>404 Error</h2>
                <h3>Page Not Found</h3>
            </section>
        );
    }
}

class Selection extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selected: null,
            menuOpened: false
        };

        this._init();
    }

    _init() {
        this.selectionMenu = React.createRef();
        this.selectionOptionsMenu = React.createRef();

        this.toggleSelectionMenu = this.toggleSelectionMenu.bind(this);
        this.closeSelectionMenuOutside = this.closeSelectionMenuOutside.bind(this);
        this.updateSelection = this.updateSelection.bind(this);

        document.addEventListener('click', this.closeSelectionMenuOutside);
    }

    componentDidUpdate(prevProps) {
        if (prevProps.options !== this.props.options) {
            this.setState({
                selected: this.props.options[0].value
            });
        }
    }

    toggleSelectionMenu() {
        this.setState({
            menuOpened: !this.state.menuOpened
        });
    }

    closeSelectionMenuOutside(event) {
        const select = this.selectionMenu.current;
        const dropdown = this.selectionOptionsMenu.current;

        if (!dropdown || !dropdown.contains(event.target) && event.target !== select) {
            this.setState({
                menuOpened: false
            });
        }
    }

    updateSelection(option, index) {
        this.setState({
            selected: option,
            menuOpened: false
        });

        this.props.setCategory(index);
    }

    render() {
        const menuSelectionClasses = ['selection'];

        if (this.state.menuOpened) {
            menuSelectionClasses.push('selection-menu-opened');
        }

        return (
            <div className={menuSelectionClasses.join(' ')}>
                <div
                    ref={this.selectionMenu}
                    className="selection-menu"
                    onClick={this.toggleSelectionMenu}
                >
                    {this.state.selected}
                    <i class="fa fa-angle-down" aria-hidden="true"></i>
                </div>
                <div ref={this.selectionOptionsMenu} className="selection-options">
                    {this.props.options.map((option, index) => {
                        return (
                            <div className="selection-option">
                                <span onClick={() => this.updateSelection(option.value, index)}>
                                    {option.value}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
}

class Loading extends React.Component {
    constructor() {
        super();
    }

    render() {
        return (
            <div class="loading">
                <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);