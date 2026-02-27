const { useState, useEffect, useRef } = React;

// ============ NAVBAR COMPONENT ============
function Navbar() {
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <nav className="bg-white shadow-md relative z-50">
            <div className="container mx-auto px-4">
                <div className="flex justify-between items-center h-20">
                    {/* Logo */}
                    <div className="flex-shrink-0">
                        <a href="/" className="text-lg font-bold text-blue-600">DAH Solar</a>
                    </div>

                    {/* Desktop Menu */}
                    <div className="hidden lg:flex space-x-6 items-center h-full text-sm">
                        <NavLink href="/" label="Home" />
                        <Divider />
                        
                        <NavDropdown label="Products" items={window.navCategories || []}>
                            {(window.navCategories || []).map(category => (
                                <div key={category.id} className="space-y-2">
                                    <h4 className="font-bold text-gray-800 border-b pb-2 hover:text-blue-600">
                                        {category.category}
                                    </h4>
                                    <div className="space-y-1">
                                        {category.types?.map(type => (
                                            <div key={type.id} className="text-sm text-gray-600 hover:text-blue-600">
                                                <i className="fa fa-angle-double-right mr-1"></i>{type.product_type}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </NavDropdown>
                        <Divider />

                        <NavDropdown label="Projects" />
                        <Divider />
                        
                        <NavDropdown label="News" />
                        <Divider />
                        
                        <NavDropdown label="DAH Solar">
                            <div className="text-sm">
                                <div className="px-4 py-2 hover:bg-gray-50 hover:text-blue-600">Overview</div>
                                <div className="px-4 py-2 hover:bg-gray-50 hover:text-blue-600">DAH Factories</div>
                                <div className="px-4 py-2 hover:bg-gray-50 hover:text-blue-600">Vision & Mission</div>
                            </div>
                        </NavDropdown>
                        <Divider />

                        <NavLink href="/contact-us" label="Contact Us" />
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="lg:hidden">
                        <button 
                            onClick={() => setMobileOpen(!mobileOpen)}
                            className="text-gray-700 hover:text-blue-600"
                        >
                            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                    </div>
                </div>

                {/* Mobile Menu */}
                {mobileOpen && (
                    <div className="lg:hidden bg-white shadow-lg p-4 space-y-4 pb-4">
                        <a href="/" className="block font-bold text-gray-700 hover:text-blue-600">Home</a>
                        <a href="/products" className="block font-bold text-gray-700 hover:text-blue-600">Products</a>
                        <a href="/projects" className="block font-bold text-gray-700 hover:text-blue-600">Projects</a>
                        <a href="/news" className="block font-bold text-gray-700 hover:text-blue-600">News</a>
                        <a href="/contact-us" className="block font-bold text-gray-700 hover:text-blue-600">Contact Us</a>
                    </div>
                )}
            </div>
        </nav>
    );
}

function NavLink({ href, label }) {
    return (
        <a href={href} className="text-gray-700 hover:text-blue-600 font-medium transition">
            {label}
        </a>
    );
}

function Divider() {
    return <span className="text-gray-300">|</span>;
}

function NavDropdown({ label, items = [], children }) {
    return (
        <div className="group relative h-full flex items-center">
            <a href="#" className="text-gray-700 group-hover:text-blue-600 font-medium transition cursor-pointer">
                {label}
            </a>
            
            {children ? (
                <div className="absolute top-full left-0 bg-white shadow-lg border-t-2 border-blue-600 hidden group-hover:block">
                    {children}
                </div>
            ) : (
                items.length > 0 && (
                    <div className="absolute top-full left-0 w-48 bg-white shadow-lg py-2 hidden group-hover:block border-t-2 border-blue-600">
                        {items.map(item => (
                            <a key={item.id} href={`#${item.slug}`} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600">
                                {item.name}
                            </a>
                        ))}
                    </div>
                )
            )}
        </div>
    );
}

// ============ CAROUSEL COMPONENT ============
function HeroCarousel({ slides = [] }) {
    const [activeSlide, setActiveSlide] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setActiveSlide(prev => (prev + 1) % slides.length);
        }, 5000);
        return () => clearInterval(interval);
    }, [slides.length]);

    const navigate = (direction) => {
        if (direction === 'next') {
            setActiveSlide(prev => (prev + 1) % slides.length);
        } else {
            setActiveSlide(prev => (prev - 1 + slides.length) % slides.length);
        }
    };

    if (!slides.length) return null;

    return (
        <div className="relative w-full h-[500px] md:h-[700px] overflow-hidden group">
            {slides.map((slide, index) => (
                <div
                    key={index}
                    className={`absolute inset-0 transition-opacity duration-1000 ease-in-out ${
                        activeSlide === index ? 'opacity-100' : 'opacity-0'
                    }`}
                >
                    <img src={slide.src} className="w-full h-full object-cover object-center" alt={slide.alt} />
                </div>
            ))}

            {/* Navigation Buttons */}
            <button
                onClick={() => navigate('prev')}
                className="absolute top-1/2 left-4 transform -translate-y-1/2 bg-black/30 hover:bg-black/50 text-white p-3 rounded-full opacity-0 group-hover:opacity-100 transition z-10"
            >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
            </button>
            <button
                onClick={() => navigate('next')}
                className="absolute top-1/2 right-4 transform -translate-y-1/2 bg-black/30 hover:bg-black/50 text-white p-3 rounded-full opacity-0 group-hover:opacity-100 transition z-10"
            >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
            </button>
        </div>
    );
}

// ============ PRODUCTS SECTION COMPONENT ============
function ProductsSection({ pvModules = [], solarSystems = [] }) {
    const [activeTab, setActiveTab] = useState('pv_module');

    const tabs = [
        { id: 'pv_module', label: 'PV Module', icon: '/static/images/our_products/pv_module.png' },
        { id: 'solar_system', label: 'Solar System', icon: '/static/images/our_products/solar_system.png' }
    ];

    const currentProducts = activeTab === 'pv_module' ? pvModules : solarSystems;

    return (
        <div className="py-16 bg-gray-50">
            <div className="container mx-auto px-4">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-gray-800 uppercase tracking-wide">Our Products</h2>
                    <p className="text-gray-500 mt-2">Quality First, Service Foremost</p>
                </div>

                {/* Tabs */}
                <ul className="flex flex-wrap justify-center border-b mb-8 gap-4">
                    {tabs.map(tab => (
                        <li
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`cursor-pointer group text-center pb-4 border-b-2 transition ${
                                activeTab === tab.id ? 'border-blue-600' : 'border-transparent hover:border-gray-300'
                            }`}
                        >
                            <img src={tab.icon} alt={tab.label} className="h-12 mx-auto mb-2 opacity-80 group-hover:opacity-100 transition" />
                            <span className={`font-medium ${activeTab === tab.id ? 'text-blue-600' : 'text-gray-700'}`}>
                                {tab.label}
                            </span>
                        </li>
                    ))}
                </ul>

                {/* Products Grid */}
                <div className="animate-fadeInUp">
                    <ul className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        {currentProducts.map(product => (
                            <ProductCard key={product.id} product={product} />
                        ))}
                    </ul>
                    <div className="text-center mt-10">
                        <a href="/products" className="inline-block px-8 py-3 border border-gray-300 text-gray-600 hover:bg-blue-600 hover:text-white hover:border-blue-600 rounded uppercase font-medium transition">
                            View More Products
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}

function ProductCard({ product }) {
    const imageUrl = product.image || product.images?.[0]?.image?.url || '/static/images/placeholder.png';
    const productUrl = `/products/${product.slug}`;
    
    return (
        <li className="group bg-white rounded-lg shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden">
            <div className="relative overflow-hidden aspect-[3/4] p-4 flex items-center justify-center bg-gray-50">
                <a href={productUrl} className="block w-full">
                    <img src={imageUrl} alt={product.name} className="w-full h-auto object-contain transform group-hover:scale-105 transition duration-500" />
                </a>
                <a href={productUrl} className="absolute bottom-4 right-4 bg-blue-600 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-blue-700">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5.951-1.429 5.951 1.429a1 1 0 001.169-1.409l-7-14z" />
                    </svg>
                </a>
            </div>
            <div className="p-4 border-t border-gray-100 text-center">
                <h4 className="font-bold text-gray-800 text-lg truncate hover:text-blue-600 transition">
                    <a href={productUrl}>{product.name}</a>
                </h4>
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">{product.description}</p>
            </div>
        </li>
    );
}

// ============ ABOUT SECTION COMPONENT ============
function AboutSection() {
    const [activeTab, setActiveTab] = useState(1);

    const aboutTabs = [
        { id: 1, label: 'Overview', icon: '/static/images/about_icon1.png' },
        { id: 2, label: 'DAH Factories', icon: '/static/images/about_icon2.png' },
        { id: 3, label: 'Certificates', icon: '/static/images/about_icon3.png' }
    ];

    return (
        <div className="py-16 bg-white">
            <div className="bg-gray-100 py-12 mb-12">
                <div className="container mx-auto px-4 text-center">
                    <h2 className="text-3xl font-bold text-gray-800 uppercase">Welcome To DAH Solar</h2>
                    <p className="text-blue-600 font-semibold mt-2">Excellent Smart PV Module Leading Runner</p>
                </div>
            </div>

            <div className="container mx-auto px-4">
                {/* Tab Nav */}
                <ul className="flex flex-wrap justify-center border-b mb-10 gap-8">
                    {aboutTabs.map(tab => (
                        <li
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`cursor-pointer text-center pb-2 border-b-2 transition ${
                                activeTab === tab.id ? 'border-blue-600' : 'border-transparent'
                            }`}
                        >
                            <img src={tab.icon} className="mx-auto mb-2 h-10" alt={tab.label} />
                            <span className="font-medium text-gray-700 hover:text-blue-600">{tab.label}</span>
                        </li>
                    ))}
                </ul>

                {/* Tab Content */}
                {activeTab === 1 && (
                    <AboutTabContent 
                        title="Who We Are"
                        image="/static/images/about-company.jpg"
                    >
                        <p className="text-gray-600 text-justify leading-relaxed">
                            Being established in 2009 in Hefei, Anhui province, DAHENG PV TECHNOLOGY CO.,LTD is a leading provider of high-efficiency crystalline silicon solar modules. We focus on the R&D and production of photovoltaic products.
                        </p>
                    </AboutTabContent>
                )}

                {activeTab === 2 && (
                    <AboutTabContent 
                        title="How We Produce"
                        image="/static/images/factories.jpg"
                    >
                        <p className="text-gray-600 text-justify leading-relaxed">
                            DAH Solar has 4 high-end technology factories with a combined annual production capacity of 2.5 GW. Our state-of-the-art facilities are equipped with the latest manufacturing technology.
                        </p>
                    </AboutTabContent>
                )}

                {activeTab === 3 && (
                    <div className="animate-fadeIn text-center">
                        <p className="mb-8 text-gray-600 max-w-3xl mx-auto">
                            DAH Solar PV modules have been certified by TUV, CEC, CE, INMETRO, FIDE, ISO19001, ISO14001, OHSMS18001, CQC and other international certifications.
                        </p>
                        <ul className="grid grid-cols-2 md:grid-cols-5 gap-4">
                            <li className="border rounded hover:shadow-lg transition p-2 bg-white">
                                <img src="/static/images/cert1.jpg" className="w-full h-auto" alt="Certification" />
                            </li>
                            <li className="border rounded hover:shadow-lg transition p-2 bg-white">
                                <img src="/static/images/cert2.jpg" className="w-full h-auto" alt="Certification" />
                            </li>
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}

function AboutTabContent({ title, image, children }) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center animate-fadeIn">
            <div className="rounded-lg overflow-hidden shadow-lg">
                <img src={image} alt={title} className="w-full h-auto hover:scale-105 transition duration-500" />
            </div>
            <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">{title}</h2>
                {children}
                <a href="#" className="text-blue-600 font-bold hover:underline mt-4 inline-block">
                    View More →
                </a>
            </div>
        </div>
    );
}

// ============ PROJECT CASES COMPONENT ============
function ProjectCases({ projects = [] }) {
    return (
        <div className="py-16 bg-gray-50">
            <div className="container mx-auto px-4">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-gray-800 uppercase">Project Cases</h2>
                    <p className="text-gray-500 mt-2 max-w-2xl mx-auto">
                        More than 120 countries have installed DAH Solar PV Modules and Solar Systems worldwide.
                    </p>
                </div>

                <ul className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {projects.map(project => (
                        <ProjectCard key={project.id} project={project} />
                    ))}
                </ul>

                <div className="text-center mt-8">
                    <a href="/projects" className="text-blue-600 font-medium hover:underline">
                        View More Projects →
                    </a>
                </div>
            </div>
        </div>
    );
}

function ProjectCard({ project }) {
    const [showOverlay, setShowOverlay] = useState(false);
    const imageUrl = project.image || project.images?.[0]?.image?.url || '/static/images/placeholder.png';
    const projectUrl = `/projects/${project.slug}`;

    return (
        <li 
            className="relative group h-64 overflow-hidden rounded-lg shadow-md cursor-pointer"
            onMouseEnter={() => setShowOverlay(true)}
            onMouseLeave={() => setShowOverlay(false)}
        >
            <img src={imageUrl} alt={project.name} className={`w-full h-full object-cover transition-transform duration-500 ${showOverlay ? 'scale-110' : ''}`} />
            
            {/* Overlay */}
            {showOverlay && (
                <div className="absolute inset-0 bg-black/60 transition-opacity duration-300 flex flex-col justify-center items-center p-6 text-center">
                    <h3 className="text-white font-bold text-xl mb-2">
                        {project.name}
                    </h3>
                    <p className="text-gray-200 text-sm mb-4 line-clamp-3">
                        {project.description?.substring(0, 120) || 'Click to view details'}
                    </p>
                    <a href={projectUrl} className="w-10 h-10 flex items-center justify-center bg-blue-600 text-white rounded-full hover:bg-blue-700 transition">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                    </a>
                </div>
            )}

            {/* Mobile Label */}
            <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-black/80 to-transparent p-4 md:hidden">
                <span className="text-white font-bold">{project.name}</span>
            </div>
        </li>
    );
}

// ============ NEWS CENTER COMPONENT ============
function NewsCenter({ news = [] }) {
    const [activeTab, setActiveTab] = useState(0);

    const tabs = [
        { id: 0, label: 'Global Exhibitions' },
        { id: 1, label: 'Events' },
        { id: 2, label: 'Social Activities' }
    ];

    // Group news by category or filter based on activeTab
    const filteredNews = news.filter((item, index) => {
        const itemsPerTab = Math.ceil(news.length / 3);
        return index >= activeTab * itemsPerTab && index < (activeTab + 1) * itemsPerTab;
    }).slice(0, 3);

    return (
        <div className="py-16 bg-white">
            <div className="container mx-auto px-4">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-gray-800 uppercase">News Center</h2>
                </div>

                {/* Tab Buttons */}
                <ul className="flex justify-center gap-2 mb-8 bg-gray-100 p-1 rounded-full w-fit mx-auto flex-wrap">
                    {tabs.map(tab => (
                        <li
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`px-6 py-2 rounded-full cursor-pointer text-sm font-medium transition whitespace-nowrap ${
                                activeTab === tab.id 
                                    ? 'bg-blue-600 text-white shadow' 
                                    : 'text-gray-600 hover:text-blue-600'
                            }`}
                        >
                            {tab.label}
                        </li>
                    ))}
                </ul>

                {/* News Grid */}
                <ul className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {filteredNews.map(item => (
                        <NewsCard key={item.id} item={item} showDate={activeTab !== 0} />
                    ))}
                </ul>
            </div>
        </div>
    );
}

function NewsCard({ item, showDate = false }) {
    const imageUrl = item.image || item.preview?.url || '/static/images/placeholder.png';
    const newsUrl = `/news/${item.slug}`;

    return (
        <li className="flex flex-col group">
            <div className="overflow-hidden rounded-lg mb-4 relative">
                <a href={newsUrl}>
                    <img 
                        src={imageUrl} 
                        alt={item.title} 
                        className="w-full h-56 object-cover transform group-hover:scale-105 transition duration-500" 
                    />
                </a>
                {showDate && item.date && (
                    <span className="absolute top-2 right-2 bg-blue-600 text-white text-xs px-2 py-1 rounded">
                        {new Date(item.date).toLocaleDateString()}
                    </span>
                )}
            </div>
            <h3 className="font-bold text-lg text-gray-800 group-hover:text-blue-600 transition mb-2">
                <a href={newsUrl}>{item.title}</a>
            </h3>
            {item.excerpt && (
                <p className="text-gray-500 text-sm line-clamp-3">{item.excerpt}</p>
            )}
        </li>
    );
}

// ============ VIDEO CENTER COMPONENT ============
function VideoCenter({ videos = [] }) {
    return (
        <div className="py-16 bg-gray-900">
            <div className="container mx-auto px-4">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-white uppercase">Video Center</h2>
                    <p className="text-gray-400 mt-2">DAH Solar Always shows the truest side to the customers.</p>
                </div>

                <ul className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {videos.map(video => (
                        <VideoCard key={video.id} video={video} />
                    ))}
                </ul>
            </div>
        </div>
    );
}

function VideoCard({ video }) {
    const imageUrl = video.thumbnail || video.preview?.url || '/static/images/placeholder.png';

    return (
        <li className="group">
            <div className="relative rounded-lg overflow-hidden shadow-lg border border-gray-700">
                <a href={`#video-${video.id}`} title={video.title} className="block">
                    <img 
                        src={imageUrl} 
                        alt={video.title} 
                        className="w-full h-64 object-cover opacity-80 group-hover:opacity-100 transition" 
                    />
                    <div className="absolute inset-0 flex items-center justify-center bg-black/20 group-hover:bg-black/40 transition">
                        <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm group-hover:scale-110 transition">
                            <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                            </svg>
                        </div>
                    </div>
                </a>
            </div>
            <h4 className="mt-4 text-white text-lg font-medium text-center group-hover:text-blue-400 transition">
                <a href={`#video-${video.id}`}>{video.title}</a>
            </h4>
        </li>
    );
}

// ============ STATS BANNER ============
function StatsBanner({ imageSrc }) {
    return (
        <div className="w-full">
            <img src={imageSrc} alt="Stats" className="w-full h-auto object-cover" />
        </div>
    );
}

// ============ MAIN HOME COMPONENT ============
function HomePage({ data = {} }) {
    return (
        <>
            <Navbar />
            <HeroCarousel slides={data.slides || []} />
            <ProductsSection pvModules={data.pvModules || []} solarSystems={data.solarSystems || []} />
            <AboutSection />
            <ProjectCases projects={data.projects || []} />
            <StatsBanner imageSrc={data.statsImage || '/static/images/stats.jpg'} />
            <NewsCenter news={data.news || []} />
            <VideoCenter videos={data.videos || []} />
        </>
    );
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        HomePage,
        Navbar,
        HeroCarousel,
        ProductsSection,
        AboutSection,
        ProjectCases,
        NewsCenter,
        VideoCenter,
        ProductCard,
        ProjectCard,
        NewsCard,
        VideoCard
    };
}
