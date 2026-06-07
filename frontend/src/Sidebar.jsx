import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <aside className="w-[260px] bg-surface-container-lowest border-r border-white/5 flex flex-col fixed inset-y-0 z-50">
      <div className="p-6">
        <h1 className="font-display-lg text-headline-md tracking-tighter text-primary-container">PRICING.AI</h1>
      </div>
      <nav className="flex-1 px-4 space-y-2 mt-4">
        <NavLink 
          to="/simulator" 
          className={({ isActive }) => 
            `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors group ${isActive ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:bg-surface-container'}`
          }
        >
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>tune</span>
          <span className="font-label-md text-label-md">Scenario Simulator</span>
        </NavLink>
        <NavLink 
          to="/analytics" 
          className={({ isActive }) => 
            `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors group ${isActive ? 'bg-secondary-container text-on-secondary-container' : 'text-on-surface-variant hover:bg-surface-container'}`
          }
        >
          <span className="material-symbols-outlined">query_stats</span>
          <span className="font-label-md text-label-md">Historical Reports</span>
        </NavLink>
        <a className="flex items-center gap-3 px-4 py-3 text-on-surface-variant hover:bg-surface-container rounded-lg transition-colors group" href="#">
          <span className="material-symbols-outlined group-hover:text-primary">settings</span>
          <span className="font-label-md text-label-md">Settings</span>
        </a>
      </nav>
      {/* Omitido el login real, solo se deja el dummy visual */}
    </aside>
  );
};

export default Sidebar;
