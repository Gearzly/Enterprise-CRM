// Mock data for the CRM dashboard

export const salesData = [
  { month: 'Jan', sales: 45000 },
  { month: 'Feb', sales: 52000 },
  { month: 'Mar', sales: 48000 },
  { month: 'Apr', sales: 61000 },
  { month: 'May', sales: 55000 },
  { month: 'Jun', sales: 67000 },
];

export const pipelineData = [
  { stage: 'Prospects', count: 45 },
  { stage: 'Qualified', count: 32 },
  { stage: 'Proposal', count: 18 },
  { stage: 'Negotiation', count: 12 },
  { stage: 'Closed Won', count: 8 },
];

export const customers = [
  {
    id: '1',
    name: 'John Smith',
    email: 'john.smith@acme.com',
    phone: '+1 (555) 123-4567',
    company: 'Acme Corp',
    status: 'active' as const,
    value: '$25,000',
    lastContact: '2 days ago',
  },
  {
    id: '2',
    name: 'Sarah Johnson',
    email: 'sarah.j@techstart.io',
    phone: '+1 (555) 234-5678',
    company: 'TechStart',
    status: 'prospect' as const,
    value: '$45,000',
    lastContact: '1 week ago',
  },
  {
    id: '3',
    name: 'Mike Chen',
    email: 'mike@innovate.com',
    phone: '+1 (555) 345-6789',
    company: 'Innovate Inc',
    status: 'active' as const,
    value: '$35,000',
    lastContact: '3 days ago',
  },
  {
    id: '4',
    name: 'Emily Davis',
    email: 'emily@futuretech.com',
    phone: '+1 (555) 456-7890',
    company: 'FutureTech',
    status: 'inactive' as const,
    value: '$15,000',
    lastContact: '2 weeks ago',
  },
];

export const activities = [
  {
    id: '1',
    type: 'email' as const,
    title: 'Follow-up email sent',
    description: 'Sent quarterly business review proposal to Acme Corp',
    user: 'John Doe',
    timestamp: '2 hours ago',
    priority: 'high' as const,
  },
  {
    id: '2',
    type: 'call' as const,
    title: 'Discovery call completed',
    description: 'Initial consultation with TechStart about their CRM needs',
    user: 'Sarah Wilson',
    timestamp: '4 hours ago',
    priority: 'medium' as const,
  },
  {
    id: '3',
    type: 'meeting' as const,
    title: 'Product demo scheduled',
    description: 'Demo meeting set for next Tuesday with Innovate Inc',
    user: 'Mike Rodriguez',
    timestamp: '1 day ago',
    priority: 'high' as const,
  },
  {
    id: '4',
    type: 'deal' as const,
    title: 'Deal closed',
    description: 'Successfully closed $50K annual contract with Global Solutions',
    user: 'Lisa Thompson',
    timestamp: '2 days ago',
    priority: 'high' as const,
  },
  {
    id: '5',
    type: 'contact' as const,
    title: 'New lead added',
    description: 'Added contact from website form submission',
    user: 'Alex Johnson',
    timestamp: '3 days ago',
    priority: 'low' as const,
  },
];

export const teamPerformance = [
  { name: 'John Doe', deals: 12, revenue: 240000, target: 200000 },
  { name: 'Sarah Wilson', deals: 8, revenue: 180000, target: 150000 },
  { name: 'Mike Rodriguez', deals: 15, revenue: 320000, target: 250000 },
  { name: 'Lisa Thompson', deals: 10, revenue: 195000, target: 180000 },
  { name: 'Alex Johnson', deals: 6, revenue: 125000, target: 120000 },
];

export const recentDeals = [
  {
    id: '1',
    name: 'Enterprise Software License',
    company: 'Global Corp',
    value: '$85,000',
    stage: 'Negotiation',
    probability: 75,
    closeDate: '2024-01-15',
    owner: 'John Doe',
  },
  {
    id: '2',
    name: 'CRM Implementation',
    company: 'TechStart',
    value: '$45,000',
    stage: 'Proposal',
    probability: 60,
    closeDate: '2024-01-20',
    owner: 'Sarah Wilson',
  },
  {
    id: '3',
    name: 'Annual Support Contract',
    company: 'Innovate Inc',
    value: '$35,000',
    stage: 'Qualified',
    probability: 40,
    closeDate: '2024-01-25',
    owner: 'Mike Rodriguez',
  },
];