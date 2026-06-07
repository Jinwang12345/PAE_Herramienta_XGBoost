import React from 'react';

const Analytics = () => {
  return (
    <main className="ml-[260px] flex-1 flex flex-col min-h-screen overflow-y-auto bg-background custom-scrollbar p-8">
      {/* Header */}
      <header className="flex items-center justify-between mb-10">
        <div>
          <h2 className="font-headline-md text-primary text-3xl font-bold">Command Center: Seasonal Analytics</h2>
        </div>
        <div className="flex items-center gap-4">
          <button className="px-4 py-2 rounded-lg border border-secondary text-secondary font-label-md flex items-center gap-2 hover:bg-secondary/10 transition-colors active:scale-95 duration-150">
            <span className="material-symbols-outlined text-[18px]">download</span>
            Download CSV
          </button>
          <button className="px-4 py-2 rounded-lg bg-secondary-container text-on-secondary-container font-label-md flex items-center gap-2 hover:opacity-90 transition-opacity active:scale-95 duration-150 shadow-[0_4px_20px_rgba(201,4,86,0.3)]">
            <span className="material-symbols-outlined text-[18px]">picture_as_pdf</span>
            Export PDF
          </button>
        </div>
      </header>

      {/* Main Dashboard View */}
      <div className="space-y-6 max-w-[1600px] w-full">
        {/* Filters Bar */}
        <div className="glass-card p-4 rounded-xl flex flex-wrap items-center gap-4">
          <div className="flex-1 min-w-[150px]">
            <label className="block text-[10px] text-on-surface-variant uppercase font-bold mb-1 ml-1">Season</label>
            <div className="relative">
              <select className="w-full bg-surface-container-high border-none text-on-surface font-label-md rounded-lg py-2 pl-3 pr-8 appearance-none focus:ring-1 focus:ring-primary/50">
                <option>2023/2024</option>
                <option>2022/2023</option>
              </select>
            </div>
          </div>
          <div className="flex-1 min-w-[150px]">
            <label className="block text-[10px] text-on-surface-variant uppercase font-bold mb-1 ml-1">Competition</label>
            <div className="relative">
              <select className="w-full bg-surface-container-high border-none text-on-surface font-label-md rounded-lg py-2 pl-3 pr-8 appearance-none focus:ring-1 focus:ring-primary/50">
                <option>All Leagues</option>
                <option>Champions League</option>
                <option>National Cup</option>
              </select>
            </div>
          </div>
          <div className="flex-1 min-w-[150px]">
            <label className="block text-[10px] text-on-surface-variant uppercase font-bold mb-1 ml-1">Sector</label>
            <div className="relative">
              <select className="w-full bg-surface-container-high border-none text-on-surface font-label-md rounded-lg py-2 pl-3 pr-8 appearance-none focus:ring-1 focus:ring-primary/50">
                <option>Grandstand South</option>
                <option>Premium Box</option>
              </select>
            </div>
          </div>
          <div className="flex-1 min-w-[150px]">
            <label className="block text-[10px] text-on-surface-variant uppercase font-bold mb-1 ml-1">Day of Week</label>
            <div className="relative">
              <select className="w-full bg-surface-container-high border-none text-on-surface font-label-md rounded-lg py-2 pl-3 pr-8 appearance-none focus:ring-1 focus:ring-primary/50">
                <option>Weekend Only</option>
                <option>Weekdays</option>
              </select>
            </div>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          <div className="glass-card p-6 rounded-xl border-l-4 border-l-primary-container relative overflow-hidden">
            <div className="flex justify-between items-start mb-2">
              <p className="font-label-sm text-on-surface-variant uppercase">Total Revenue</p>
              <span className="material-symbols-outlined text-primary-fixed-dim">payments</span>
            </div>
            <p className="font-numeric-xl text-primary">$42.8M</p>
            <div className="flex items-center mt-2 text-tertiary-fixed-dim font-label-sm">
              <span className="material-symbols-outlined text-sm mr-1">trending_up</span>
              <span>+12.4% vs LY</span>
            </div>
          </div>

          <div className="glass-card p-6 rounded-xl border-l-4 border-l-tertiary relative overflow-hidden">
            <div className="flex justify-between items-start mb-2">
              <p className="font-label-sm text-on-surface-variant uppercase">Avg Occupancy</p>
              <span className="material-symbols-outlined text-tertiary-fixed-dim">group</span>
            </div>
            <p className="font-numeric-xl text-tertiary">91.4%</p>
            <div className="flex items-center mt-2 text-tertiary-fixed-dim font-label-sm">
              <span className="material-symbols-outlined text-sm mr-1">trending_up</span>
              <span>+4.2% vs LY</span>
            </div>
          </div>

          <div className="glass-card p-6 rounded-xl border-l-4 border-l-secondary relative overflow-hidden">
            <div className="flex justify-between items-start mb-2">
              <p className="font-label-sm text-on-surface-variant uppercase">Avg Ticket Price</p>
              <span className="material-symbols-outlined text-secondary">local_activity</span>
            </div>
            <p className="font-numeric-xl text-secondary">$124.50</p>
            <div className="flex items-center mt-2 text-on-surface-variant font-label-sm">
              <span className="material-symbols-outlined text-sm mr-1">horizontal_rule</span>
              <span>Stable</span>
            </div>
          </div>

          <div className="glass-card p-6 rounded-xl border-l-4 border-l-on-tertiary-container relative overflow-hidden">
            <div className="flex justify-between items-start mb-2">
              <p className="font-label-sm text-on-surface-variant uppercase">Retention Rate</p>
              <span className="material-symbols-outlined text-on-tertiary-container">cached</span>
            </div>
            <p className="font-numeric-xl text-on-tertiary-container">88.2%</p>
            <div className="flex items-center mt-2 text-error font-label-sm">
              <span className="material-symbols-outlined text-sm mr-1">trending_down</span>
              <span>-1.1% vs LY</span>
            </div>
          </div>
        </div>

        {/* Bottom Sections Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Performance by Competition */}
          <div className="lg:col-span-1 glass-card p-6 rounded-xl">
            <h3 className="font-label-md text-on-surface uppercase tracking-wider mb-4">Performance by Competition</h3>
            <div className="space-y-4">
              <div className="p-3 bg-surface-container-low rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-label-md">Premier League</span>
                  <span className="font-label-md text-primary">$28.4M</span>
                </div>
                <div className="w-full h-1.5 bg-surface-variant rounded-full overflow-hidden">
                  <div className="h-full bg-primary-container w-[85%] rounded-full shadow-[0_0_10px_rgba(255,215,0,0.4)]"></div>
                </div>
              </div>
              <div className="p-3 bg-surface-container-low rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-label-md">Champions League</span>
                  <span className="font-label-md text-secondary">$10.2M</span>
                </div>
                <div className="w-full h-1.5 bg-surface-variant rounded-full overflow-hidden">
                  <div className="h-full bg-secondary w-[60%] rounded-full shadow-[0_0_10px_rgba(201,4,86,0.4)]"></div>
                </div>
              </div>
              <div className="p-3 bg-surface-container-low rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-label-md">National Cup</span>
                  <span className="font-label-md text-tertiary-fixed-dim">$4.2M</span>
                </div>
                <div className="w-full h-1.5 bg-surface-variant rounded-full overflow-hidden">
                  <div className="h-full bg-tertiary-fixed-dim w-[35%] rounded-full shadow-[0_0_10px_rgba(0,218,243,0.4)]"></div>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Matches Table */}
          <div className="lg:col-span-2 glass-card rounded-xl overflow-hidden">
            <div className="p-6 border-b border-white/5 flex justify-between items-center">
              <h3 className="font-label-md text-on-surface uppercase tracking-wider">Recent Matches Performance</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-surface-container-low/50 font-label-sm text-on-surface-variant uppercase tracking-tighter">
                  <tr>
                    <th className="px-6 py-4">Match Details</th>
                    <th className="px-6 py-4">Competition</th>
                    <th className="px-6 py-4 text-right">Attendance</th>
                    <th className="px-6 py-4 text-right">Revenue</th>
                    <th className="px-6 py-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 font-label-md">
                  <tr className="hover:bg-white/5 transition-colors cursor-pointer group">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-bold">VS</div>
                        <div>
                          <p className="text-on-surface">Home vs Real Madrid</p>
                          <p className="text-[10px] text-on-surface-variant uppercase">May 14, 2024</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4"><span className="px-2 py-1 bg-secondary-container/20 text-secondary rounded text-[11px] font-bold">CL</span></td>
                    <td className="px-6 py-4 text-right">98,245</td>
                    <td className="px-6 py-4 text-right text-primary">$3,421,000</td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center">
                        <span className="flex items-center gap-1 text-[11px] text-tertiary-fixed-dim bg-on-tertiary/20 px-2 py-0.5 rounded-full">
                          <span className="w-1.5 h-1.5 rounded-full bg-tertiary-fixed-dim animate-pulse"></span>
                          OPTIMAL
                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr className="hover:bg-white/5 transition-colors cursor-pointer">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-bold">VS</div>
                        <div>
                          <p className="text-on-surface">Home vs Atletico</p>
                          <p className="text-[10px] text-on-surface-variant uppercase">May 10, 2024</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4"><span className="px-2 py-1 bg-primary-container/20 text-primary-fixed-dim rounded text-[11px] font-bold">LL</span></td>
                    <td className="px-6 py-4 text-right">92,400</td>
                    <td className="px-6 py-4 text-right text-primary">$2,110,000</td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center">
                        <span className="flex items-center gap-1 text-[11px] text-tertiary-fixed-dim bg-on-tertiary/20 px-2 py-0.5 rounded-full">
                          <span className="w-1.5 h-1.5 rounded-full bg-tertiary-fixed-dim"></span>
                          OPTIMAL
                        </span>
                      </div>
                    </td>
                  </tr>
                  <tr className="hover:bg-white/5 transition-colors cursor-pointer">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center font-bold">VS</div>
                        <div>
                          <p className="text-on-surface">Home vs Getafe</p>
                          <p className="text-[10px] text-on-surface-variant uppercase">May 03, 2024</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4"><span className="px-2 py-1 bg-primary-container/20 text-primary-fixed-dim rounded text-[11px] font-bold">LL</span></td>
                    <td className="px-6 py-4 text-right">74,100</td>
                    <td className="px-6 py-4 text-right text-primary">$1,240,000</td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center">
                        <span className="flex items-center gap-1 text-[11px] text-on-surface-variant bg-surface-variant px-2 py-0.5 rounded-full">
                          UNDER
                        </span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Analytics;
