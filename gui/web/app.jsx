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

        this.MAX_KEYWORDS = 3;

        this.state = {
            categories: [],
            documents: [],
            keywords: [],
            selectedKeywords: {},
            catIndex: 0,
            searchValue: '',
            loading: true,
            menuOpened: false
        };

        this._init();
    }

    _init() {
        this.getCategories = this.getCategories.bind(this);
        this.getDocuments = this.getDocuments.bind(this);
        this.setCategory = this.setCategory.bind(this);
        this.searchKeywords = this.searchKeywords.bind(this);
        this.getKeywords = this.getKeywords.bind(this);
        this.searchByKeywords = this.searchByKeywords.bind(this);
        this.selectKeyword = this.selectKeyword.bind(this);
        this.removeKeyword = this.removeKeyword.bind(this);
        this.closeKeywordsListOutside = this.closeKeywordsListOutside.bind(this);

        this.keywordsList = React.createRef();
        document.addEventListener('click', this.closeKeywordsListOutside);
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
        this.setState({
            documents: docs
        });
    }

    getDocumentsByCategory(category) {
        eel.py_request('/articles', {
            has_category: category
        })(this.getDocuments);
    }

    searchKeywords(event) {
        const value = event.target.value;

        if (value.length > 2) {
            this.setState({
                loading: true,
                searchValue: event.target.value,
                menuOpened: true
            }, () => {
                eel.py_request('/keywords', {
                    start: this.state.searchValue
                })(this.getKeywords);
            });
        } else {
            this.setState({
                menuOpened: false,
                searchValue: value
            });
        }
    }

    getKeywords(keywords) {
        this.setState({
            keywords: keywords,
            loading: false
        })
    }

    searchByKeywords() {
        if (Object.keys(this.state.selectedKeywords).length > 0) {
            this.setState({
                documents: []
            }, () => {
                eel.py_request('/articles', {
                    has_keyword: Object.keys(this.state.selectedKeywords)
                })(this.getDocuments);
            });
        }
    }

    selectKeyword(keyword) {
        const selected = this.state.selectedKeywords;

        if (Object.keys(selected).length === 3) {
            return;
        }

        if (selected.hasOwnProperty(keyword.id)) {
            return;
        }

        this.setState({
            selectedKeywords: {
                ...this.state.selectedKeywords,
                [keyword.id]: keyword.value
            },
            searchValue: '',
            menuOpened: false
        });
    }

    removeKeyword(key) {
        const selected = this.state.selectedKeywords;
        delete selected[key];
        this.setState({
            selectedKeywords: selected
        });
    }

    closeKeywordsListOutside(event) {
        const dropdown = this.keywordsList.current;

        if (!dropdown || !dropdown.contains(event.target)) {
            this.setState({
                menuOpened: false
            });
        }
    }

    render() {
        return (
            <section class="documents">
                <header>
                    <Selection options={this.state.categories} setCategory={this.setCategory} />
                    <div className="search">
                        <div className="selected-keywords">
                            {
                                Object.keys(this.state.selectedKeywords).map((key) => {
                                    return (
                                        <span className="keyword-chip">
                                            {this.state.selectedKeywords[key]}
                                            <span
                                                className="delete-keyword"
                                                onClick={() => this.removeKeyword(key)}
                                            >
                                                ×
                                            </span>
                                        </span>
                                    );
                                })
                            }
                        </div>
                        <input
                            className="search-input"
                            placeholder={
                                Object.keys(this.state.selectedKeywords).length === 0 &&
                                'Seleziona una o più keywords...'
                            }
                            value={this.state.searchValue}
                            onChange={this.searchKeywords}
                        />
                        <span className="search-button" onClick={this.searchByKeywords}>
                            <i className="fa fa-search" aria-hidden="true"></i>
                        </span>
                        {
                            this.state.menuOpened &&
                            <div ref={this.keywordsList} className="keywords-list">
                                {
                                    this.state.loading ?
                                        <Loading /> :
                                        this.state.keywords.length > 0 ?
                                            this.state.keywords.map((key) => {
                                                return (
                                                    <div className="keyword">
                                                        <span onClick={() => this.selectKeyword(key)}>
                                                            <span class="highlight">
                                                                {this.state.searchValue}
                                                            </span>
                                                            {key.value.substring(this.state.searchValue.length)}
                                                        </span>
                                                    </div>
                                                );
                                            }) :
                                            <div className="keywords-not-found">No keywords</div>
                                }
                            </div>
                        }
                    </div>
                </header>
                {this.state.documents.length === 0 ?
                    <Loading /> :
                    this.state.documents.map(doc => {
                        return (
                            <article className="document">
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
            <section className="not-found">
                <i className="fa fa-meh-o" aria-hidden="true"></i>
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
            <div className="loading">
                <i className="fa fa-spinner fa-spin fa-3x fa-fw"></i>
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);