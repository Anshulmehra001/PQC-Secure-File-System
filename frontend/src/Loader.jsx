import React from 'react';

export default function Loader({ message = "Encrypting with Kyber512..." }) {
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
      <p className="loader-message">{message}</p>
    </div>
  );
}
