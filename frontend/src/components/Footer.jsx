const Footer = ({ isDarkMode }) => {
  return (
    <footer className={`py-6 px-4 text-center mt-16 ${
      isDarkMode ? 'bg-gray-800 text-gray-300' : 'bg-gray-100 text-gray-700'
    }`}>
      <p className="text-sm">
        Developed by{" "}
        <a
          href="https://www.narenderkeswani.com"
          target="_blank"
          rel="noopener noreferrer"
          className={`underline font-medium hover:text-blue-500 transition-colors ${
            isDarkMode ? 'text-gray-300' : 'text-gray-700'
          }`}
        >
          Narender Keswani
        </a>{" "}
        • All rights reserved © {new Date().getFullYear()}
      </p>
    </footer>
  );
};

export default Footer;
