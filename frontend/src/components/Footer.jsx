import React from "react";

const Footer = () => {
  return (
    <footer className="border-t bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50 mt-16">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col items-center justify-center space-y-3">
                     {/* Logo and Brand */}
           <div className="flex items-center space-x-2">
             <img 
               src="/uwear transparent logo.PNG"
               alt="Uwear Logo"
               className="h-10"
             />
             <span className="text-sm font-semibold text-foreground">Uwear</span>
           </div>
          
          {/* Copyright */}
          <p className="text-xs text-muted-foreground text-center">
            © {new Date().getFullYear()} Uwear. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
