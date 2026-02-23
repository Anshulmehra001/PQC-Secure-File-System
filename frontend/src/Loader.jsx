import React, { useState, useEffect } from 'react';

export default function Loader({ message = "Processing...", steps = [] }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [displayMessage, setDisplayMessage] = useState(message);

  useEffect(() => {
    if (steps.length > 0) {
      const interval = setInterval(() => {
        setCurrentStep((prev) => {
          const next = (prev + 1) % steps.length;
          setDisplayMessage(steps[next]);
          return next;
        });
      }, 800);
      
      setDisplayMessage(steps[0]);
      return () => clearInterval(interval);
    } else {
      setDisplayMessage(message);
    }
  }, [steps, message]);

  return (
    <div className="loader-overlay">
      <div className="loader-3d">
        <div className="box box0"><div></div></div>
        <div className="box box1"><div></div></div>
        <div className="box box2"><div></div></div>
        <div className="box box3"><div></div></div>
        <div className="box box4"><div></div></div>
        <div className="box box5"><div></div></div>
        <div className="box box6"><div></div></div>
        <div className="box box7"><div></div></div>
        <div className="ground"><div></div></div>
      </div>
      <p className="loader-message">{displayMessage}</p>
      {steps.length > 0 && (
        <div className="loader-steps-indicator">
          {steps.map((_, index) => (
            <span 
              key={index} 
              className={`step-dot ${index === currentStep ? 'active' : ''}`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
