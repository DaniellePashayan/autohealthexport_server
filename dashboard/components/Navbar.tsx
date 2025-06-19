const Navbar = () => {
  return (
    <nav className="flex items-center justify-between p-4 bg-white border-b">
      <h1 className="text-xl font-bold">My App</h1>
      <ul className="flex space-x-4">
        <li>
          <a href="#" className="text-gray-700 hover:text-blue-500">Home</a>
        </li>
        <li>
          <a href="#" className="text-gray-700 hover:text-blue-500">About</a>
        </li>
        <li>
          <a href="#" className="text-gray-700 hover:text-blue-500">Contact</a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
