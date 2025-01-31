const { useState, useEffect } = React;

// Create icon components manually since we can't use Lucide React directly
const ServerIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
        <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
        <line x1="6" y1="6" x2="6" y2="6"></line>
        <line x1="6" y1="18" x2="6" y2="18"></line>
    </svg>
);

const CloudIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path>
    </svg>
);

const DatabaseIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
    </svg>
);

const PowerIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
        <line x1="12" y1="2" x2="12" y2="12"></line>
    </svg>
);

const SpinnerIcon = ({ className }) => (
    <svg className={`animate-spin ${className}`} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 22C6.5 22 2 17.5 2 12S6.5 2 12 2s10 4.5 10 10" />
    </svg>
);

const Alert = ({ children, className = "" }) => (
    <div className={`p-4 rounded-lg border dark:border-gray-700 ${className}`}>
        <div className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
            {children}
        </div>
    </div>
);

const AlertDescription = ({ children }) => (
    <div className="text-sm text-gray-800 dark:text-gray-100">{children}</div>
);

// Add a Notification component
const Notification = ({ error, loading }) => {
    if (!error && !loading) return null;
    
    return (
        <div className="fixed top-4 right-4 flex flex-col gap-2 z-50">
            {error && (
                <div className="bg-red-100 text-red-700 px-4 py-2 rounded shadow-lg">
                    Error: {error}
                </div>
            )}
        </div>
    );
};

// Add an eye icon component
const EyeIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
        <circle cx="12" cy="12" r="3" />
    </svg>
);

const EyeOffIcon = ({ className }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
        <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68" />
        <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61" />
        <line x1="2" y1="2" x2="22" y2="22" />
    </svg>
);

// Update the SettingsDialog component
const SettingsDialog = ({ isOpen, onClose, settings }) => {
    if (!isOpen || !settings) return null;
    
    const [visibleSecrets, setVisibleSecrets] = useState({});

    const toggleSecret = (key) => {
        setVisibleSecrets(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    const renderValue = (key, value) => {
        const isSecret = key.includes('KEY') || key.includes('TOKEN');
        if (!isSecret) return value;

        return (
            <div className="flex items-center gap-2">
                <span className="font-mono text-sm">
                    {visibleSecrets[key] ? value : '••••••••'}
                </span>
                <button
                    type="button"
                    onClick={() => toggleSecret(key)}
                    className="text-gray-400 hover:text-gray-600"
                >
                    {visibleSecrets[key] ? 
                        <EyeOffIcon className="h-4 w-4" /> : 
                        <EyeIcon className="h-4 w-4" />
                    }
                </button>
            </div>
        );
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-semibold dark:text-white">Settings</h2>
                    <button 
                        type="button"
                        onClick={onClose}
                        className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
                    >
                        ×
                    </button>
                </div>
                <div className="space-y-4">
                    <div>
                        <h3 className="font-medium mb-2 dark:text-white">Environment Variables</h3>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded space-y-2">
                            {Object.entries(settings.env || {}).map(([key, value]) => (
                                <div key={key} className="flex justify-between items-center">
                                    <span className="font-mono text-sm">{key}</span>
                                    {renderValue(key, value)}
                                </div>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h3 className="font-medium mb-2 dark:text-white">Service Configuration</h3>
                        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded space-y-2">
                            <div className="flex justify-between dark:text-gray-300">
                                <span>Consul URL</span>
                                <span className="text-blue-600 dark:text-blue-400">http://consul:8500</span>
                            </div>
                            <div className="flex justify-between dark:text-gray-300">
                                <span>API Port</span>
                                <span>3000</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Add ThemeContext at the top of the file
const ThemeContext = React.createContext({
    theme: 'light',
    toggleTheme: () => {}
});

// Add ThemeProvider component
const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState('light');

    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        document.documentElement.classList.toggle('dark');
    };

    useEffect(() => {
        // Check system preference
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setTheme('dark');
            document.documentElement.classList.add('dark');
        }
    }, []);

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

// Update the ThemeToggle component with monochrome icons
const ThemeToggle = () => {
    const { theme, toggleTheme } = React.useContext(ThemeContext);
    
    return (
        <button
            type="button"
            onClick={toggleTheme}
            className="relative inline-flex items-center justify-center w-10 h-10 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
            aria-label="Toggle theme"
        >
            {/* Sun icon */}
            <span className={`absolute transition-opacity ${theme === 'dark' ? 'opacity-0' : 'opacity-100'}`}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-600">
                    <circle cx="12" cy="12" r="5" />
                    <line x1="12" y1="1" x2="12" y2="3" />
                    <line x1="12" y1="21" x2="12" y2="23" />
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                    <line x1="1" y1="12" x2="3" y2="12" />
                    <line x1="21" y1="12" x2="23" y2="12" />
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
                </svg>
            </span>
            
            {/* Moon icon */}
            <span className={`absolute transition-opacity ${theme === 'light' ? 'opacity-0' : 'opacity-100'}`}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-400">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
                </svg>
            </span>
        </button>
    );
};

const Dashboard = () => {
    const [servers, setServers] = useState({
        app: { status: 'stopped' },
        gpu: { status: 'stopped' }
    });
    const [stateStatus, setStateStatus] = useState({
        consul: false,
        s3: false
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);
    const [settings, setSettings] = useState(null);
    const [showSettings, setShowSettings] = useState(false);

    const fetchStatus = async (showLoading = false) => {
        try {
            if (showLoading) setLoading(true);
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.success) {
                // Parse the output to determine server status
                const appRunning = data.output.includes('app-server');
                const gpuRunning = data.output.includes('gpu-server');
                
                setServers({
                    app: { 
                        status: appRunning ? 'running' : 'stopped',
                        ip: appRunning ? 'Connected' : null
                    },
                    gpu: { 
                        status: gpuRunning ? 'running' : 'stopped',
                        ip: gpuRunning ? 'Connected' : null
                    }
                });

                // Use the services status from the API
                setStateStatus({
                    consul: data.services.consul,
                    s3: data.services.s3
                });
                setLastUpdated(new Date().toLocaleTimeString());
            }
        } catch (err) {
            setError(err.message);
        } finally {
            if (showLoading) setLoading(false);
        }
    };

    const fetchSettings = async () => {
        try {
            const response = await fetch('/api/settings');
            const data = await response.json();
            if (data.success) {
                setSettings(data.settings);
            }
        } catch (err) {
            setError(err.message);
        }
    };

    const handleServerAction = async (type, action) => {
        try {
            setLoading(true);
            const response = await fetch(`/api/${action}/${type}`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.success) {
                await fetchStatus();
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus(true);
        fetchSettings();
        const interval = setInterval(() => fetchStatus(false), 30000);
        return () => clearInterval(interval);
    }, []);

    const ServerCard = ({ type, server }) => (
        <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                    <ServerIcon className={server.status === 'running' ? 'text-green-500' : 'text-gray-400 dark:text-gray-500'} />
                    <div>
                        <h3 className="font-medium dark:text-white">{type.toUpperCase()} Server</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{server.ip || 'Not running'}</p>
                    </div>
                </div>
                <button 
                    type="button"
                    onClick={() => handleServerAction(type, server.status === 'running' ? 'stop' : 'start')}
                    className={`p-2 rounded ${
                        server.status === 'running' 
                            ? 'bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400' 
                            : 'bg-green-100 dark:bg-green-900/50 text-green-600 dark:text-green-400'
                    }`}
                    disabled={loading}
                >
                    <PowerIcon size={16} />
                </button>
            </div>
        </div>
    );

    const handleSettingsClick = () => {
        setShowSettings(true);
    };

    return (
        <div className="p-8 bg-gray-50 dark:bg-gray-900 min-h-screen">
            <Notification error={error} loading={loading} />
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold dark:text-white">AINI Dashboard</h1>
                <div className="flex items-center gap-4">
                    <ThemeToggle />
                    {lastUpdated && (
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                            Last updated: {lastUpdated}
                        </span>
                    )}
                    <button 
                        type="button"
                        onClick={() => fetchStatus(true)}
                        className="px-3 py-1 bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-300 rounded hover:bg-blue-100 dark:hover:bg-blue-800 flex items-center gap-2"
                        disabled={loading}
                    >
                        {loading && <SpinnerIcon className="h-4 w-4" />}
                        Refresh
                    </button>
                </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <ServerCard type="app" server={servers.app} />
                <ServerCard type="gpu" server={servers.gpu} />
            </div>

            <div className="space-y-4">
                <h2 className="text-xl font-semibold mb-4 dark:text-white">State Management</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <a 
                        href="http://consul:8500" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="block transition-transform hover:scale-102"
                    >
                        <Alert className={`${
                            stateStatus.consul 
                                ? 'bg-green-50 dark:bg-green-950 hover:bg-green-100 dark:hover:bg-green-900' 
                                : 'bg-red-50 dark:bg-red-950 hover:bg-red-100 dark:hover:bg-red-900'
                            } transition-colors`}>
                            <DatabaseIcon className="h-4 w-4 text-gray-800 dark:text-gray-100" />
                            <AlertDescription>
                                Consul: {stateStatus.consul ? 'Connected' : 'Disconnected'}
                            </AlertDescription>
                        </Alert>
                    </a>
                    <Alert className={`${
                        stateStatus.s3 
                            ? 'bg-green-50 dark:bg-green-950 hover:bg-green-100 dark:hover:bg-green-900' 
                            : 'bg-gray-50 dark:bg-gray-950 hover:bg-gray-100 dark:hover:bg-gray-900'
                        } transition-colors`}>
                        <CloudIcon className="h-4 w-4 text-gray-800 dark:text-gray-100" />
                        <AlertDescription>
                            S3 Storage: {stateStatus.s3 ? 'Connected' : 'Not Configured'}
                        </AlertDescription>
                    </Alert>
                </div>
            </div>

            <div className="mt-8">
                <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <button type="button" className="p-4 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/50">
                        View Logs
                    </button>
                    <button type="button" className="p-4 bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-300 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/50">
                        Check Config
                    </button>
                    <button type="button" className="p-4 bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-300 rounded-lg hover:bg-purple-100 dark:hover:bg-purple-900/50">
                        View State
                    </button>
                    <button 
                        type="button" 
                        className="p-4 bg-orange-50 dark:bg-orange-900/30 text-orange-600 dark:text-orange-300 rounded-lg hover:bg-orange-100 dark:hover:bg-orange-900/50"
                        onClick={handleSettingsClick}
                    >
                        Settings
                    </button>
                </div>
            </div>
            <SettingsDialog 
                isOpen={showSettings} 
                onClose={() => setShowSettings(false)} 
                settings={settings}
            />
        </div>
    );
};

// Update the root render to include ThemeProvider
ReactDOM.render(
    <ThemeProvider>
        <Dashboard />
    </ThemeProvider>,
    document.getElementById('root')
); 