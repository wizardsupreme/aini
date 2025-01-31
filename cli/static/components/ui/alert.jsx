const Alert = ({ children, className = "" }) => (
  <div className={`p-4 rounded-lg border ${className}`}>
    <div className="flex items-center gap-2">
      {children}
    </div>
  </div>
);

const AlertDescription = ({ children }) => (
  <div className="text-sm">{children}</div>
);

export { Alert, AlertDescription }; 