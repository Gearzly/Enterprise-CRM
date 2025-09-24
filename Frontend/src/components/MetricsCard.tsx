import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { motion } from 'motion/react';

interface MetricsCardProps {
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down' | 'neutral';
  icon?: React.ReactNode;
  percentage?: string;
  isLoading?: boolean;
}

export function MetricsCard({ title, value, change, trend, icon, percentage, isLoading = false }: MetricsCardProps) {
  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus;
  const trendColor = trend === 'up' ? 'text-emerald-600 dark:text-emerald-400' : trend === 'down' ? 'text-red-600 dark:text-red-400' : 'text-muted-foreground';
  const trendBg = trend === 'up' ? 'bg-emerald-50 dark:bg-emerald-950' : trend === 'down' ? 'bg-red-50 dark:bg-red-950' : 'bg-muted';
  const iconBg = trend === 'up' ? 'bg-emerald-100 dark:bg-emerald-900' : trend === 'down' ? 'bg-red-100 dark:bg-red-900' : 'bg-muted';
  
  if (isLoading) {
    return (
      <Card className="p-6 animate-pulse">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="h-4 bg-muted rounded w-3/4 mb-3"></div>
            <div className="h-8 bg-muted rounded w-1/2 mb-3"></div>
            <div className="h-4 bg-muted rounded w-2/3"></div>
          </div>
          <div className="w-12 h-12 bg-muted rounded-full"></div>
        </div>
      </Card>
    );
  }
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={{ y: -4 }}
      className="group"
    >
      <Card className="p-6 h-full bg-gradient-to-br from-card to-card/50 border-border/50 shadow-sm hover:shadow-md transition-all duration-300 group-hover:border-border">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <p className="text-sm font-medium text-muted-foreground">{title}</p>
              {percentage && (
                <Badge variant="outline" className="text-xs">
                  {percentage}
                </Badge>
              )}
            </div>
            
            <motion.p 
              className="text-3xl font-bold text-foreground mb-3"
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              {value}
            </motion.p>
            
            <motion.div 
              className={`flex items-center gap-2 px-3 py-1.5 rounded-full ${trendBg} w-fit`}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: 0.2 }}
            >
              <div className={`p-1 rounded-full ${iconBg}`}>
                <TrendIcon className={`w-3 h-3 ${trendColor}`} />
              </div>
              <span className={`text-sm font-medium ${trendColor}`}>{change}</span>
            </motion.div>
          </div>
          
          {icon && (
            <motion.div 
              className="p-3 rounded-xl bg-primary/10 text-primary group-hover:scale-110 transition-transform duration-300"
              whileHover={{ rotate: 10 }}
            >
              {icon}
            </motion.div>
          )}
        </div>
        
        {/* Progress bar for visual appeal */}
        <div className="mt-4 w-full h-1 bg-muted rounded-full overflow-hidden">
          <motion.div
            className={`h-full ${trend === 'up' ? 'bg-emerald-500' : trend === 'down' ? 'bg-red-500' : 'bg-muted-foreground'}`}
            initial={{ width: 0 }}
            animate={{ width: `${Math.abs(parseFloat(percentage || '50'))}%` }}
            transition={{ duration: 1, delay: 0.5 }}
          />
        </div>
      </Card>
    </motion.div>
  );
}