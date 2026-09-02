import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface Record {
  id: number;
  reference_date: string;
  deliveries: number;
  note: string;
  employee: { name: string; department: string };
}

interface Summary {
  total_records: number;
  total_deliveries: number;
  chart_data: { department: string; deliveries: number }[];
}

export default function App() {
  const [records, setRecords] = useState<Record[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8080';
        const [resRecords, resSummary] = await Promise.all([
          fetch(`${apiUrl}/records`),
          fetch(`${apiUrl}/summary`)
        ]);

        if (!resRecords.ok || !resSummary.ok) throw new Error("Erro na API");

        setRecords(await resRecords.json());
        setSummary(await resSummary.json());
      } catch (err) {
        setError(true);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="p-10 text-center text-xl">Carregando painel...</div>;
  if (error) return <div className="p-10 text-center text-red-500 text-xl">Erro ao carregar os dados. Verifique se a API está rodando.</div>;

  return (
    <div className="container mx-auto p-8 font-sans">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Painel Gerencial de Entregas</h1>

      {/* Cartões de Resumo */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
          <h2 className="text-gray-500 text-sm uppercase font-bold">Total de Registros</h2>
          <p className="text-4xl font-bold text-gray-800">{summary?.total_records || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
          <h2 className="text-gray-500 text-sm uppercase font-bold">Total de Entregas</h2>
          <p className="text-4xl font-bold text-gray-800">{summary?.total_deliveries || 0}</p>
        </div>
      </div>

      {/* Gráfico */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Entregas por Departamento</h2>
        <div className="h-64 w-full">
          {summary?.chart_data && summary.chart_data.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={summary.chart_data}>
                <XAxis dataKey="department" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="deliveries" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">Sem dados para o gráfico</div>
          )}
        </div>
      </div>

      {/* Tabela de Registros */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 text-gray-600 uppercase text-sm leading-normal">
              <th className="py-3 px-6 font-bold">Funcionário</th>
              <th className="py-3 px-6 font-bold">Departamento</th>
              <th className="py-3 px-6 font-bold text-center">Data</th>
              <th className="py-3 px-6 font-bold text-center">Entregas</th>
            </tr>
          </thead>
          <tbody className="text-gray-700 text-sm font-light">
            {records.length === 0 ? (
              <tr><td colSpan={4} className="py-4 text-center">Nenhum registro encontrado.</td></tr>
            ) : (
              records.map((rec) => (
                <tr key={rec.id} className="border-b border-gray-200 hover:bg-gray-50">
                  <td className="py-3 px-6 whitespace-nowrap font-medium">{rec.employee.name}</td>
                  <td className="py-3 px-6">{rec.employee.department}</td>
                  <td className="py-3 px-6 text-center">{rec.reference_date}</td>
                  <td className="py-3 px-6 text-center font-bold">{rec.deliveries}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}