import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  BarChart, 
  Bar,
  Area,
  AreaChart
} from 'recharts';
import { TrendingUp, TrendingDown, MoreHorizontal, Download, Maximize2, Info } from 'lucide-react';
import { motion } from 'motion/react';
import { useState } from 'react';

interface SalesChartProps {
  title: string;
  type?: 'line' | 'bar' | 'area';
  data: any[];
  dataKey: string;
  xAxisKey: string;
  subtitle?: string;
  showGradient?: boolean;
}

export function SalesChart({ 
  title, 
  type = 'line', 
  data, 
  dataKey, 
  xAxisKey, 
  subtitle,
  showGradient = true 
}: SalesChartProps) {
  const [chartType, setChartType] = useState(type);
  
  // Calculate trend
  const currentValue = data[data.length - 1]?.[dataKey] || 0;
  const previousValue = data[data.length - 2]?.[dataKey] || 0;
  const trend = currentValue > previousValue ? 'up' : 'down';
  const trendPercent = previousValue ? ((currentValue - previousValue) / previousValue * 100).toFixed(1) : '0';
  
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-popover border border-border rounded-lg shadow-lg p-3">
          <p className="font-medium">{`${label}`}</p>
          <p className="text-primary">
            {`${dataKey}: ${payload[0].value.toLocaleString()}`}
          </p>
        </div>
      );
    }
    return null;
  };

  const renderChart = () => {
    const commonProps = {
      data,
      margin: { top: 5, right: 30, left: 20, bottom: 5 }
    };

    switch (chartType) {
      case 'bar':
        return (
          <BarChart {...commonProps}>
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
            <XAxis 
              dataKey={xAxisKey} 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey={dataKey} 
              fill={showGradient ? "url(#barGradient)" : "hsl(var(--primary))"} 
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        );
      
      case 'area':
        return (
          <AreaChart {...commonProps}>
            <defs>
              <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0.1}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
            <XAxis 
              dataKey={xAxisKey} 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area 
              type="monotone" 
              dataKey={dataKey} 
              stroke="hsl(var(--primary))"
              fillOpacity={1}
              fill="url(#areaGradient)"
              strokeWidth={3}
            />
          </AreaChart>
        );
        
      default:
        return (
          <LineChart {...commonProps}>
            <defs>
              <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="hsl(var(--primary))" />
                <stop offset="100%" stopColor="hsl(var(--chart-1))" />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
            <XAxis 
              dataKey={xAxisKey} 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis 
              stroke="hsl(var(--muted-foreground))" 
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey={dataKey} 
              stroke={showGradient ? "url(#lineGradient)" : "hsl(var(--primary))"}
              strokeWidth={3}
              dot={{ 
                fill: 'hsl(var(--primary))', 
                strokeWidth: 2, 
                stroke: 'hsl(var(--background))',
                r: 6
              }}
              activeDot={{ 
                r: 8, 
                stroke: 'hsl(var(--primary))',
                strokeWidth: 2,
                fill: 'hsl(var(--background))'
              }}
            />
          </LineChart>
        );
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="p-6 h-full bg-gradient-to-br from-card to-card/50 border-border/50 shadow-sm hover:shadow-md transition-all duration-300">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <h3 className="text-xl font-semibold text-foreground">{title}</h3>
              <Badge variant="outline" className="text-xs">
                {trend === 'up' ? '+' : ''}{trendPercent}%
              </Badge>
            </div>
            {subtitle && (
              <p className="text-sm text-muted-foreground">{subtitle}</p>
            )}
            <div className="flex items-center gap-2">
              {trend === 'up' ? (
                <TrendingUp className="w-4 h-4 text-emerald-500" />
              ) : (
                <TrendingDown className="w-4 h-4 text-red-500" />
              )}
              <span className={`text-sm font-medium ${trend === 'up' ? 'text-emerald-600' : 'text-red-600'}`}>
                {trend === 'up' ? 'Trending up' : 'Trending down'} vs last period
              </span>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            {/* Chart type selector */}
            <div className="flex items-center bg-muted rounded-lg p-1">
              <Button
                variant={chartType === 'line' ? 'default' : 'ghost'}
                size="sm"
                className="h-7 px-2 text-xs"
                onClick={() => setChartType('line')}
              >
                Line
              </Button>
              <Button
                variant={chartType === 'area' ? 'default' : 'ghost'}
                size="sm"
                className="h-7 px-2 text-xs"
                onClick={() => setChartType('area')}
              >
                Area
              </Button>
              <Button
                variant={chartType === 'bar' ? 'default' : 'ghost'}
                size="sm"
                className="h-7 px-2 text-xs"
                onClick={() => setChartType('bar')}
              >
                Bar
              </Button>
            </div>
            
            <Button variant="ghost" size="sm">
              <Download className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="sm">
              <Maximize2 className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="sm">
              <MoreHorizontal className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Chart */}
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            {renderChart()}
          </ResponsiveContainer>
        </div>

        {/* Footer Stats */}
        <div className="mt-6 pt-4 border-t border-border/50">
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-sm text-muted-foreground">Peak</p>
              <p className="text-lg font-semibold">
                ${Math.max(...data.map(d => d[dataKey])).toLocaleString()}
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-muted-foreground">Average</p>
              <p className="text-lg font-semibold">
                ${Math.round(data.reduce((sum, d) => sum + d[dataKey], 0) / data.length).toLocaleString()}
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-muted-foreground">Total</p>
              <p className="text-lg font-semibold">
                ${data.reduce((sum, d) => sum + d[dataKey], 0).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}