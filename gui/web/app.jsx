class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activeRoute: location.hash,
            document: {}
        };

        this.setActiveRoute = this.setActiveRoute.bind(this);
        this.setDocument = this.setDocument.bind(this);

        window.addEventListener('hashchange', this.setActiveRoute);
    }

    setActiveRoute() {
        this.setState({
            activeRoute: location.hash
        });
    }

    setDocument(document) {
        this.setState({
            document: document
        });
    }

    render() {
        return (
            <main>
                <Sidebar />
                {(route => {
                    switch (route) {
                        case '':
                        case '#articles':
                        case (route.match(/#articles(\?(keywords|category)=?(\w+,?)+)/) || {}).input:
                            return <ArticlesSection setDocument={this.setDocument} />
                        case (route.match(/#articles\/\w+/) || {}).input:
                            return <ArticleDetails id={route.split('/')[1]} />
                        case '#classification':
                            return <Classification />
                        default:
                            return <NotFound />
                    }
                })(this.state.activeRoute)}
            </main>
        );
    }
}

class Sidebar extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <aside class="sidebar">
                <div class="logo">
                    <h1>Kency</h1>
                </div>
                <nav class="nav">
                    <h2 className="title">Main Menu</h2>
                    <NavMenu />
                </nav>
            </aside>
        );
    }
}

class NavMenu extends React.Component {
    constructor(props) {
        super(props);

        this.categories = [
            {
                hash: '#articles',
                name: 'Articles',
                icon: 'fa-file-text'
            },
            {
                hash: '#classification',
                name: 'Text Classification',
                icon: 'fa-cogs'
            },
            {
                hash: '#query',
                name: 'Query Builder',
                icon: 'fa-database'
            },
            {
                hash: '#about',
                name: 'About Us',
                icon: 'fa-users'
            },
        ]
    }

    render() {
        return (
            <ul className="nav-menu">
                {this.categories.map((cat, i) => {
                    return <NavMenuItem item={cat} isFirst={i === 0} />
                })}
            </ul>
        );
    }
}

class NavMenuItem extends React.Component {
    constructor(props) {
        super(props);
    }

    isActive(route) {
        return (location.hash === '' && this.props.isFirst) || location.hash.startsWith(route);
    }

    render() {
        return (
            <li className={this.isActive(this.props.item.hash) && 'active'}>
                <a href={this.props.item.hash}>
                    <i className={'fa ' + this.props.item.icon} aria-hidden="true"></i>
                    {this.props.item.name}
                </a>
            </li>
        );
    }
}

class ArticlesSection extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            category: '',
            keywords: [],
            showDetails: false,
            document: {}
        }

        this.setCategory = this.setCategory.bind(this);
        this.setKeywords = this.setKeywords.bind(this);
    }

    setCategory(category) {
        this.setState({
            category: category.id,
            keywords: []
        }, () => {
            location.hash = `#articles?category=${category.value}`
        });
    }

    setKeywords(keywords) {
        this.setState({
            keywords: keywords,
            category: ''
        }, () => {
            location.hash = `#articles?keywords=${keywords.map(key => {
                return key.value
            }).join(',')}`
        });
    }

    render() {
        return (
            <section className="documents">
                <ArticlesHeader
                    setCategory={this.setCategory}
                    setKeywords={this.setKeywords}
                />
                <ArticlesList
                    category={this.state.category}
                    keywords={this.state.keywords}
                    setCategory={this.setCategory}
                    setKeywords={this.setKeywords}
                    setDocument={this.props.setDocument}
                />
            </section>
        );
    }
}

class ArticlesHeader extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            categories: []
        };

        this.getCategories();
    }

    getCategories() {
        eel.py_request('/categories')(categories => {
            this.setState({
                categories: categories
            }, () => {
                this.props.setCategory(categories[0])
            });
        });
    }

    render() {
        return (
            <header>
                <Selection
                    options={this.state.categories}
                    setOption={this.props.setCategory}
                />
                <Search setKeywords={this.props.setKeywords} />
            </header>
        );
    }
}

class ArticlesList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            documents: [],
            loading: true
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps !== this.props) {
            this.setState({
                loading: true
            }, () => {
                if (this.props.keywords.length > 0) {
                    this.getDocumentsByKeywords();
                } else {
                    this.getDocumentsByCategory();
                }
            });
        }
    }

    getDocumentsByCategory() {
        eel.py_request('/articles', {
            has_category: this.props.category
        })(documents => {
            this.setState({
                documents: documents,
                loading: false
            });
        });
    }

    getDocumentsByKeywords() {
        eel.py_request('/articles', {
            has_keyword: this.props.keywords.map(key => { return key.id })
        })(documents => {
            this.setState({
                documents: documents,
                loading: false
            });
        });
    }

    render() {
        return (
            <React.Fragment>
                {this.state.loading ?
                    <Loading /> :
                    this.state.documents.map(doc => {
                        return (
                            <article className="document">
                                <h2>
                                    <a
                                        href={'#articles/' + doc.entity_name}
                                        onClick={() => this.props.setDocument(doc)}
                                    >
                                        {doc.entity_name}
                                    </a>
                                </h2>
                                <p>{doc.has_content.slice(0, 249) + '...'}</p>
                            </article>
                        );
                    })}
            </React.Fragment>
        );
    }
}

class ArticleDetails extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            document: null,
            loading: true
        };

        this.getDocumentDetails();
    }

    componentDidUpdate(prevProps) {
        if (prevProps !== this.props) {
            this.setState({
                loading: true
            }, () => {
                this.getDocumentDetails();
            });
        }
    }

    getDocumentDetails() {
        eel.py_request('/article', {
            id: this.props.id
        })(document => {
            this.setState({
                document: document,
                loading: false
            });
        });
    }

    render() {
        return (
            <section className="article-details">
                {this.state.loading ?
                    <Loading /> :
                    <React.Fragment>
                        <article className="document">
                            <section>
                                <h2>
                                    {this.state.document.entity_name}
                                    <span className="document-category">
                                        {this.state.document.has_category.has_name}
                                    </span>
                                </h2>
                                <p>{this.state.document.has_content}</p>
                            </section>
                            <section>
                                <h2>Related Links</h2>
                            </section>
                            <section>
                                <h2>Related Articles</h2>
                            </section>
                        </article>
                        <aside className="document-keywords">
                            <h3>Keywords</h3>
                            <ul>
                                {this.state.document.has_keyword.map(key => {
                                    return (
                                        <li>{key.has_value}</li>
                                    );
                                })}
                            </ul>
                        </aside>
                    </React.Fragment>
                }
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
    constructor(props) {
        super(props);
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
            selected: '',
            menuOpened: false
        };

        this.selectRef = React.createRef();
        this.selectOptionsRef = React.createRef();

        this.toggleSelectionMenu = this.toggleSelectionMenu.bind(this);
        this.closeOnClickOutside = this.closeOnClickOutside.bind(this);
        this.updateSelection = this.updateSelection.bind(this);

        document.addEventListener('click', this.closeOnClickOutside);
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

    closeOnClickOutside(event) {
        const select = this.selectRef.current;
        const dropdown = this.selectOptionsRef.current;

        if (!dropdown || !dropdown.contains(event.target) && event.target !== select) {
            this.setState({
                menuOpened: false
            });
        }
    }

    updateSelection(option) {
        this.setState({
            selected: option.value,
            menuOpened: false
        }, () => {
            this.props.setOption(option);
        });
    }

    render() {
        const menuSelectionClasses = ['selection'];

        if (this.state.menuOpened) {
            menuSelectionClasses.push('selection-menu-opened');
        }

        return (
            <div className={menuSelectionClasses.join(' ')}>
                <div
                    ref={this.selectRef}
                    className="selection-menu"
                    onClick={this.toggleSelectionMenu}
                >
                    {this.state.selected}
                    <i class="fa fa-angle-down" aria-hidden="true"></i>
                </div>
                <div ref={this.selectOptionsRef} className="selection-options">
                    {this.props.options.map(option => {
                        return (
                            <div className="selection-option">
                                <span onClick={() => this.updateSelection(option)}>
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

class Search extends React.Component {
    constructor(props) {
        super(props);

        this.MAX_KEYWORDS = 3;

        this.state = {
            keywords: [],
            selectedKeywords: [],
            value: '',
            loading: true,
            menuOpened: false
        };

        this.keywordsListRef = React.createRef();

        this.isSearching = this.isSearching.bind(this);
        this.getKeywords = this.getKeywords.bind(this);
        this.addKeyword = this.addKeyword.bind(this);
        this.removeKeyword = this.removeKeyword.bind(this);
        this.filterByKeywords = this.filterByKeywords.bind(this);
        this.closeOnClickOutside = this.closeOnClickOutside.bind(this);

        document.addEventListener('click', this.closeOnClickOutside);
    }

    isMenuOpened() {
        return this.state.keywords.length > 0;
    }

    find(keyword) {
        return this.state.selectedKeywords.some(key => {
            return key.id === keyword.id;
        });
    }

    remove(keyword) {
        return this.state.selectedKeywords.filter(key => {
            return key.id !== keyword.id;
        });
    }

    isSearching(event) {
        if (event.target.value.length > 2) {
            this.setState({
                menuOpened: true,
                value: event.target.value
            }, this.getKeywords);
        } else {
            this.setState({
                menuOpened: false,
                value: event.target.value
            });
        }
    }

    getKeywords() {
        eel.py_request('/keywords', {
            start: this.state.value
        })(keywords => {
            this.setState({
                keywords: keywords,
                loading: false
            });
        });
    }

    addKeyword(keyword) {
        if (this.state.selectedKeywords.length === this.MAX_KEYWORDS) {
            return;
        }

        if (this.find(keyword)) {
            return;
        }

        this.setState({
            selectedKeywords: this.state.selectedKeywords.concat(keyword),
            value: '',
            menuOpened: false
        });
    }

    removeKeyword(keyword) {
        this.setState({
            selectedKeywords: this.remove(keyword)
        });
    }

    filterByKeywords() {
        if (this.state.selectedKeywords.length > 0) {
            this.props.setKeywords(this.state.selectedKeywords);
        }
    }

    closeOnClickOutside(event) {
        const dropdown = this.keywordsListRef.current;

        if (!dropdown || !dropdown.contains(event.target)) {
            this.setState({
                menuOpened: false
            });
        }
    }

    render() {
        return (
            <div className="search">
                <div className="selected-keywords">
                    {this.state.selectedKeywords.map(key => {
                        return (
                            <span className="keyword-chip">
                                {key.value}
                                <span
                                    className="delete-keyword"
                                    onClick={() => this.removeKeyword(key)}
                                >×</span>
                            </span>
                        );
                    })}
                </div>
                <input
                    className="search-input"
                    placeholder={!this.isMenuOpened() && 'Select one or more keywords...'}
                    value={this.state.value}
                    onChange={this.isSearching}
                />
                <span className="search-button" onClick={this.filterByKeywords}>
                    <i className="fa fa-search" aria-hidden="true"></i>
                </span>
                {this.state.menuOpened &&
                    <div ref={this.keywordsListRef} className="keywords-list">
                        {this.state.loading ?
                            <Loading /> :
                            this.state.keywords.length > 0 ?
                                this.state.keywords.map(key => {
                                    return (
                                        <div className="keyword">
                                            <span onClick={() => this.addKeyword(key)}>
                                                <span class="highlight">
                                                    {this.state.value}
                                                </span>
                                                {key.value.substring(this.state.value.length)}
                                            </span>
                                        </div>
                                    );
                                }) :
                                <div className="keywords-not-found">No keywords</div>}
                    </div>}
            </div>
        );
    }
}

class Loading extends React.Component {
    constructor(props) {
        super(props);
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