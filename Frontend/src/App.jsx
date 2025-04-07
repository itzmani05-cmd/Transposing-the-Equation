import { useState } from "react";

function App() {
  const [equation, setEquation] = useState("");
  const [variable, setVariable] = useState("");
  const [result, setResult] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const solvingEqu = async () => {
    if (!equation || !variable) {
      alert("Enter both the Equation and Variable!");
      setResult([]);
      setError("");
      return;
    }
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          equation: equation.trim(), 
          solve_for: variable.trim()
        }),
      });

      const data = await response.json();
      console.log("Response Data:", data);

      if (data.detail) {
        setError(data.detail);
        setResult([]);
      } else {
        setResult(data.solution);
        setError("");
      }
    } catch (err) {
      setError("Unable to connect to the server!");
      setResult([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800">
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
          <h1 className="text-2xl font-bold text-center mb-4">Equation Solver</h1>
          <input
            type="text"
            value={equation}
            onChange={(e) => setEquation(e.target.value)}
            placeholder="Enter equation like 2y + 3 = x"
            className="w-full px-4 py-2 border rounded-md mb-4"
          />

          <input
            type="text"
            value={variable}
            onChange={(e) => setVariable(e.target.value)}
            placeholder="Enter variable like y"
            className="w-full px-4 py-2 border rounded-md mb-4"
          />

          <button
            onClick={solvingEqu}
            className="w-full bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Solving..." : "Solve"}
          </button>

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-300 text-red-800 rounded-xl shadow-sm">
              <strong className="block font-semibold mb-1">Error:</strong>
              <p className="text-sm">{error}</p>
            </div>
          )}


          {result.length > 0 && (
          <div className="mt-6 p-6 bg-green-50 border border-green-300 rounded-xl shadow-sm">
            <h3 className="text-lg font-semibold text-green-800 mb-2">Rearranged Equation:</h3>
            <ul className="list-disc list-inside text-green-700 space-y-1">
              {result.map((res, index) => (
                <li key={index} className="text-base">
                  {res}
                </li>
              ))}
            </ul>
          </div>
        )}



        </div>
      </div>
    </div>
  );
}

export default App;
