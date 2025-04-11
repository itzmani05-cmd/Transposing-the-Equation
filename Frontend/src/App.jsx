import React, { useState } from "react";

const keys = {
  mathPad: [
    ["x","7", "8", "9", "clr"],
    ["y","4", "5", "6", "+", "-"],
    ["z","1", "2", "3", "*", "%"],
    ["a", "b", "0", "(", ")", "=", "abc"]
  ],
  qwerty: [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
    ["clr", "z", "x", "c", "v", "b", "n", "m", "del"],
    ["123", "space", "enter"]
  ]
};

export default function CustomKeyboard() {
  const [input, setInput] = useState("");
  const [variable, setVariable] = useState("");
  const [activeField, setActiveField] = useState("equation");
  const [showQwerty, setShowQwerty] = useState(false);
  const [result, setResult] = useState("");

  const handleKeyPress = (key) => {
    const value = activeField === "equation" ? input : variable;
    const setValue = activeField === "equation" ? setInput : setVariable;

    if (key === "space") return setValue(value + " ");
    if (key === "del") return setValue(value.slice(0, -1));
    if (key === "clr") return setValue("");
    if (key === "abc") return setShowQwerty(true);
    if (key === "123") return setShowQwerty(false);
    if (["shift", "emoji", "enter"].includes(key)) return;
    const FunctionsKey = ["log", "sqrt", "sin", "cos", "tan", "ln"];
    if (FunctionsKey.includes(key)) return setValue(value + key + "(");
    setValue(value + key);
  };

  const renderButton = (key, index) => {
    const isSpace = key === "space";
    const isEnter = key === "enter";
    const wideKeys = ["space", "enter", "abc", "clr", "del", "123"];
    const isWide = wideKeys.includes(key);

    return (
      <button
        key={index}
        onClick={() => handleKeyPress(key)}
        className={`py-3 px-4 m-1 rounded-xl bg-gray-100 text-gray-800 text-lg font-medium shadow-sm hover:bg-gray-200 transition
          ${isSpace ? "w-[240px]" : isEnter ? "w-[100px]" : isWide ? "w-[64px]" : "w-[48px]"}`}
      >
        {key === "space" ? "" : key}
      </button>
    );
  };

  const solveEquation = async () => {
    if (!variable) {
      setResult("Please enter a variable to solve for.");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          equation: input,
          solve_for: variable
        })
      });

      const data = await res.json();
      if (res.ok) {
        setResult(data.solution.join("\n"));
      } else {
        setResult("Error: " + data.detail);
      }
    } catch (err) {
      setResult("Error: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center p-5">
      <div className="w-full max-w-[800px] bg-white rounded-3xl shadow-lg p-6 space-y-5">
        <h1 className="text-2xl font-bold text-center text-gray-800">Transposing the Equation</h1>

        {/* Equation Input Display */}
        <div
          onClick={() => setActiveField("equation")}
          className={`p-3 border rounded-xl text-lg shadow-inner bg-white cursor-pointer ${
            activeField === "equation" ? "border-blue-500" : "border-gray-300"
          }`}
        >
          {input || "Enter equation"}
        </div>

        {/* Variable Input Display */}
        <div
          onClick={() => setActiveField("variable")}
          className={`p-3 border rounded-xl text-lg shadow-inner bg-white cursor-pointer ${
            activeField === "variable" ? "border-blue-500" : "border-gray-300"
          }`}
        >
          {variable || "Enter variable to solve for"}
        </div>

        {/* Solve Button */}
        <button
          onClick={solveEquation}
          className="w-full py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition"
        >
          Solve
        </button>

        {/* Display the result*/}
        <div className="p-4 bg-gray-100 text-gray-800 rounded-xl text-base whitespace-pre-line min-h-[60px]">
          {result}
        </div>

        {/* Custom Keyboard */}
        {!showQwerty ? (
          <div className="grid grid-cols-5 gap-2 bg-gray-50 p-5 rounded-xl shadow-inner">
            {keys.mathPad.flat().map(renderButton)}
          </div>
        ) : (
          <div className="space-y-2 bg-gray-50 p-4 rounded-xl shadow-inner">
            {keys.qwerty.map((row, rowIndex) => (
              <div key={rowIndex} className="flex justify-center gap-1">
                {row.map((key, index) => renderButton(key, `${rowIndex}-${index}`))}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
