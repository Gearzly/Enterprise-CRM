import { Card } from './ui/card';
import { Skeleton } from './ui/skeleton';
import { motion } from 'motion/react';

export function MetricsCardSkeleton() {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <Skeleton className="h-4 w-3/4 mb-3" />
          <Skeleton className="h-8 w-1/2 mb-3" />
          <Skeleton className="h-4 w-2/3" />
        </div>
        <Skeleton className="w-12 h-12 rounded-full" />
      </div>
    </Card>
  );
}

export function ChartSkeleton() {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="space-y-2">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-32" />
        </div>
        <div className="flex items-center gap-2">
          <Skeleton className="h-8 w-20" />
          <Skeleton className="h-8 w-8" />
          <Skeleton className="h-8 w-8" />
        </div>
      </div>
      <Skeleton className="h-80 w-full" />
      <div className="mt-6 pt-4 border-t">
        <div className="grid grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="text-center">
              <Skeleton className="h-4 w-16 mx-auto mb-2" />
              <Skeleton className="h-6 w-20 mx-auto" />
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <Skeleton className="h-6 w-48 mb-2" />
          <Skeleton className="h-4 w-32" />
        </div>
        <div className="flex items-center gap-2">
          <Skeleton className="h-8 w-20" />
          <Skeleton className="h-8 w-24" />
        </div>
      </div>
      
      <div className="space-y-3">
        {[...Array(rows)].map((_, i) => (
          <div key={i} className="flex items-center gap-4 p-3 border rounded-lg">
            <Skeleton className="w-10 h-10 rounded-full" />
            <div className="flex-1">
              <Skeleton className="h-4 w-3/4 mb-2" />
              <Skeleton className="h-3 w-1/2" />
            </div>
            <Skeleton className="h-6 w-16" />
            <Skeleton className="h-8 w-8" />
          </div>
        ))}
      </div>
    </Card>
  );
}

export function ActivityFeedSkeleton() {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <Skeleton className="h-6 w-48 mb-2" />
          <Skeleton className="h-4 w-32" />
        </div>
        <div className="flex items-center gap-2">
          <Skeleton className="h-8 w-20" />
          <Skeleton className="h-8 w-24" />
        </div>
      </div>
      
      <div className="space-y-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="flex items-start gap-3 p-3 rounded-lg">
            <Skeleton className="w-10 h-10 rounded-full" />
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-5 w-16" />
              </div>
              <Skeleton className="h-3 w-full mb-2" />
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Skeleton className="w-5 h-5 rounded-full" />
                  <Skeleton className="h-3 w-20" />
                </div>
                <Skeleton className="h-3 w-16" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="p-6 space-y-8 bg-gradient-to-br from-background to-muted/20 min-h-screen">
      {/* Header Skeleton */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <Skeleton className="h-10 w-64" />
            <Skeleton className="h-6 w-12" />
          </div>
          <Skeleton className="h-5 w-96" />
          <div className="flex items-center gap-4">
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-4 w-24" />
          </div>
        </div>
        <div className="flex items-center gap-3">
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-9 w-20" />
          ))}
        </div>
      </div>

      {/* Metrics Cards Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <MetricsCardSkeleton key={i} />
        ))}
      </div>

      {/* Charts and Activity Feed Skeleton */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2">
          <ChartSkeleton />
        </div>
        <div className="xl:col-span-1">
          <ActivityFeedSkeleton />
        </div>
      </div>

      {/* Table Skeleton */}
      <TableSkeleton />
    </div>
  );
}

export function PageLoadingSpinner() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <motion.div
        className="flex flex-col items-center gap-4"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div
          className="w-16 h-16 border-4 border-primary/20 border-t-primary rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        <motion.p
          className="text-muted-foreground"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          Loading your dashboard...
        </motion.p>
      </motion.div>
    </div>
  );
}

export function ErrorState({ 
  title = "Something went wrong",
  description = "We encountered an error while loading this page.",
  onRetry 
}: {
  title?: string;
  description?: string;
  onRetry?: () => void;
}) {
  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-96 p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="text-center space-y-4">
        <div className="w-16 h-16 mx-auto bg-destructive/10 rounded-full flex items-center justify-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring" }}
            className="text-destructive text-2xl"
          >
            ⚠️
          </motion.div>
        </div>
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          <p className="text-muted-foreground mt-1">{description}</p>
        </div>
        {onRetry && (
          <motion.button
            className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            onClick={onRetry}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Try Again
          </motion.button>
        )}
      </div>
    </motion.div>
  );
}

export function EmptyState({ 
  title = "No data available",
  description = "There's no data to display at the moment.",
  actionLabel,
  onAction
}: {
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}) {
  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-96 p-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="text-center space-y-4">
        <div className="w-16 h-16 mx-auto bg-muted rounded-full flex items-center justify-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring" }}
            className="text-muted-foreground text-2xl"
          >
            📊
          </motion.div>
        </div>
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          <p className="text-muted-foreground mt-1">{description}</p>
        </div>
        {actionLabel && onAction && (
          <motion.button
            className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            onClick={onAction}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {actionLabel}
          </motion.button>
        )}
      </div>
    </motion.div>
  );
}