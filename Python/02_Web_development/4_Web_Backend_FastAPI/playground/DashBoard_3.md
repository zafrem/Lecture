```
import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import axios from "axios";

const StatCard = ({ title, value, delta }) => (
  <div className="bg-white border rounded p-3">
    <p className="text-sm text-gray-500">{title}</p>
    <div className="flex justify-between items-center mt-1">
      <h3 className="text-lg font-semibold">{value}</h3>
      <span className={`text-xs ${delta > 0 ? "text-green-500" : "text-red-500"}`}>
        {delta > 0 ? `+${delta}%` : `${delta}%`}
      </span>
    </div>
  </div>
);

const AnalyticsChart = ({ data }) => (
  <div className="bg-white border rounded p-3 h-64">
    <h2 className="text-base font-semibold mb-2">일별 사용자 수</h2>
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <XAxis dataKey="name" stroke="#999" />
        <YAxis stroke="#999" />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

const DataTable = ({ rows }) => {
  const downloadCSV = () => {
    const csv = ["날짜,사용자,전환율", ...rows.map(r => `${r.date},${r.users},${r.conversion}`)].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white border rounded overflow-auto">
      <div className="flex justify-between items-center p-3">
        <h2 className="text-base font-semibold">상세 데이터</h2>
        <button
          onClick={downloadCSV}
          className="text-sm bg-blue-500 text-white px-3 py-1 rounded"
        >
          CSV 다운로드
        </button>
      </div>
      <table className="w-full text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 text-left">날짜</th>
            <th className="p-2 text-left">사용자</th>
            <th className="p-2 text-left">전환율</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx} className="border-t">
              <td className="p-2">{row.date}</td>
              <td className="p-2">{row.users}</td>
              <td className="p-2">{row.conversion}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default function DashboardPage() {
  const [stats, setStats] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [startDate, setStartDate] = useState("2025-03-24");
  const [endDate, setEndDate] = useState("2025-03-28");

  useEffect(() => {
    axios.get(`/api/dashboard/stats?start=${startDate}&end=${endDate}`).then(res => {
      setStats(res.data.stats);
      setChartData(res.data.chart);
      setTableData(res.data.table);
    });
  }, [startDate, endDate]);

  return (
    <div className="p-4 bg-gray-100 min-h-screen space-y-4">
      <div className="flex flex-col md:flex-row gap-4">
        <div>
          <label className="text-sm mr-1">시작일</label>
          <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="border rounded px-2 py-1" />
        </div>
        <div>
          <label className="text-sm mr-1">종료일</label>
          <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="border rounded px-2 py-1" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {stats.map((stat, idx) => (
          <StatCard key={idx} title={stat.title} value={stat.value} delta={stat.delta} />
        ))}
      </div>

      <AnalyticsChart data={chartData} />

      <DataTable rows={tableData} />
    </div>
  );
}
```