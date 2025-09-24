import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Textarea } from '../../components/ui/textarea';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Label } from '../../components/ui/label';
import { Switch } from '../../components/ui/switch';
import { Progress } from '../../components/ui/progress';
import { Checkbox } from '../../components/ui/checkbox';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { 
  FolderOpen, Plus, Filter, Search, Eye, Edit, Trash2, Star, 
  Clock, User, Tag, Globe, FileText, BarChart3, 
  TrendingUp, Share2, Copy, Archive, CheckCircle,
  AlertCircle, XCircle, PlayCircle, PauseCircle, RefreshCw,
  Zap, Settings, Download, Upload, PieChart, Activity,
  MapPin, DollarSign, ShoppingCart, Mail, Phone, Smartphone,
  Video, Mic, Camera, Monitor, Headphones, MessageSquare,
  ExternalLink, QrCode, Ticket, Gift, Award, Target,
  Handshake, Building, Calendar, CreditCard, Briefcase,
  Network, Shield, Key, Lock, Unlock, UserCheck,
  TrendingDown, AlertTriangle, Info, Heart, ThumbsUp,
  FileCheck, FileX, FilePlus, Folder, FolderPlus,
  Link, Unlink, Send, Inbox, Outbox, Bell, BellOff,
  Image, FileImage, FileVideo, FileAudio, File,
  Layers, Package, Palette, Brush, Scissors, Crop,
  Move, RotateCcw, ZoomIn, ZoomOut, Maximize,
  Grid, List, Calendar as CalendarIcon, Users,
  HardDrive, Cloud, Server, Database, Cpu,
  Wifi, WifiOff, Signal, Battery, BatteryLow,
  Timer, Stopwatch, AlarmClock, History, Bookmark
} from 'lucide-react';

interface Asset {
  id: number;
  name: string;
  type: 'image' | 'video' | 'audio' | 'document' | 'template' | 'brand-asset';
  category: string;
  format: string;
  size: number;
  dimensions?: string;
  duration?: string;
  url: string;
  thumbnail?: string;
  description: string;
  tags: string[];
  createdBy: string;
  createdAt: string;
  lastModified: string;
  downloads: number;
  views: number;
  status: 'active' | 'archived' | 'pending' | 'expired';
  version: string;
  license: 'internal' | 'commercial' | 'creative-commons' | 'royalty-free';
  campaign?: string;
  folder: string;
  isShared: boolean;
  sharedWith: string[];
  approvalStatus: 'approved' | 'pending' | 'rejected' | 'not-required';
  approvedBy?: string;
  expiryDate?: string;
  usage: {
    campaigns: number;
    emails: number;
    social: number;
    web: number;
  };
}

interface ResourceAllocation {
  id: number;
  resourceName: string;
  resourceType: 'budget' | 'personnel' | 'equipment' | 'software' | 'venue' | 'external';
  allocatedTo: string;
  project: string;
  campaign: string;
  amount: number;
  unit: string;
  startDate: string;
  endDate: string;
  status: 'allocated' | 'in-use' | 'completed' | 'cancelled' | 'overdue';
  utilization: number;
  cost: number;
  budgetRemaining: number;
  assignedBy: string;
  notes: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

interface Folder {
  id: number;
  name: string;
  path: string;
  parentId?: number;
  assetCount: number;
  size: number;
  createdBy: string;
  createdAt: string;
  isShared: boolean;
  permissions: string[];
}

export function ResourcesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedAssets, setSelectedAssets] = useState<number[]>([]);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedFolder, setSelectedFolder] = useState<number | null>(null);
  const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false);
  const [isCreateFolderDialogOpen, setIsCreateFolderDialogOpen] = useState(false);
  const [isAllocateResourceDialogOpen, setIsAllocateResourceDialogOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('assets');

  const assets: Asset[] = [
    {
      id: 1,
      name: 'Summer Campaign Hero Image',
      type: 'image',
      category: 'Campaign Assets',
      format: 'PNG',
      size: 2048000,
      dimensions: '1920x1080',
      url: '/api/placeholder/400/300',
      thumbnail: '/api/placeholder/200/150',
      description: 'Main hero image for summer 2024 campaign',
      tags: ['summer', 'campaign', 'hero', 'banner'],
      createdBy: 'Sarah Johnson',
      createdAt: '2024-01-15',
      lastModified: '2024-01-20',
      downloads: 45,
      views: 128,
      status: 'active',
      version: '1.2',
      license: 'internal',
      campaign: 'Summer 2024',
      folder: 'Campaign Assets',
      isShared: true,
      sharedWith: ['Marketing Team', 'Design Team'],
      approvalStatus: 'approved',
      approvedBy: 'Mike Chen',
      usage: {
        campaigns: 3,
        emails: 8,
        social: 12,
        web: 5
      }
    },
    {
      id: 2,
      name: 'Product Demo Video',
      type: 'video',
      category: 'Product Content',
      format: 'MP4',
      size: 15728640,
      dimensions: '1920x1080',
      duration: '2:45',
      url: '/api/placeholder/video',
      thumbnail: '/api/placeholder/200/150',
      description: 'Comprehensive product demonstration video',
      tags: ['product', 'demo', 'tutorial', 'features'],
      createdBy: 'David Kim',
      createdAt: '2024-01-10',
      lastModified: '2024-01-18',
      downloads: 23,
      views: 89,
      status: 'active',
      version: '1.0',
      license: 'commercial',
      folder: 'Product Content',
      isShared: false,
      sharedWith: [],
      approvalStatus: 'approved',
      approvedBy: 'Emily Rodriguez',
      usage: {
        campaigns: 2,
        emails: 4,
        social: 6,
        web: 8
      }
    },
    {
      id: 3,
      name: 'Brand Guidelines Document',
      type: 'document',
      category: 'Brand Assets',
      format: 'PDF',
      size: 5242880,
      url: '/api/placeholder/document',
      description: 'Complete brand guidelines and style guide',
      tags: ['brand', 'guidelines', 'style', 'identity'],
      createdBy: 'Lisa Wang',
      createdAt: '2023-12-01',
      lastModified: '2024-01-05',
      downloads: 67,
      views: 156,
      status: 'active',
      version: '2.1',
      license: 'internal',
      folder: 'Brand Assets',
      isShared: true,
      sharedWith: ['All Teams'],
      approvalStatus: 'approved',
      approvedBy: 'Sarah Johnson',
      usage: {
        campaigns: 15,
        emails: 25,
        social: 18,
        web: 12
      }
    },
    {
      id: 4,
      name: 'Email Template - Newsletter',
      type: 'template',
      category: 'Email Templates',
      format: 'HTML',
      size: 102400,
      url: '/api/placeholder/template',
      description: 'Responsive newsletter email template',
      tags: ['email', 'newsletter', 'template', 'responsive'],
      createdBy: 'Ahmed Hassan',
      createdAt: '2024-01-22',
      lastModified: '2024-01-25',
      downloads: 12,
      views: 34,
      status: 'pending',
      version: '1.0',
      license: 'internal',
      folder: 'Email Templates',
      isShared: false,
      sharedWith: [],
      approvalStatus: 'pending',
      usage: {
        campaigns: 0,
        emails: 8,
        social: 0,
        web: 0
      }
    },
    {
      id: 5,
      name: 'Company Logo Vector',
      type: 'brand-asset',
      category: 'Brand Assets',
      format: 'SVG',
      size: 51200,
      url: '/api/placeholder/logo',
      description: 'Official company logo in vector format',
      tags: ['logo', 'brand', 'vector', 'official'],
      createdBy: 'Design Team',
      createdAt: '2023-06-15',
      lastModified: '2023-12-10',
      downloads: 234,
      views: 567,
      status: 'active',
      version: '3.0',
      license: 'internal',
      folder: 'Brand Assets',
      isShared: true,
      sharedWith: ['All Teams'],
      approvalStatus: 'approved',
      approvedBy: 'CEO',
      usage: {
        campaigns: 45,
        emails: 89,
        social: 67,
        web: 123
      }
    }
  ];

  const allocations: ResourceAllocation[] = [
    {
      id: 1,
      resourceName: 'Q1 Campaign Budget',
      resourceType: 'budget',
      allocatedTo: 'Sarah Johnson',
      project: 'Spring Launch',
      campaign: 'Spring 2024 Campaign',
      amount: 50000,
      unit: 'USD',
      startDate: '2024-01-01',
      endDate: '2024-03-31',
      status: 'in-use',
      utilization: 65,
      cost: 32500,
      budgetRemaining: 17500,
      assignedBy: 'Mike Chen',
      notes: 'Primary budget allocation for spring product launch',
      priority: 'high'
    },
    {
      id: 2,
      resourceName: 'Video Production Team',
      resourceType: 'personnel',
      allocatedTo: 'David Kim',
      project: 'Product Demo Series',
      campaign: 'Product Education',
      amount: 3,
      unit: 'people',
      startDate: '2024-02-01',
      endDate: '2024-02-28',
      status: 'allocated',
      utilization: 0,
      cost: 15000,
      budgetRemaining: 15000,
      assignedBy: 'Emily Rodriguez',
      notes: 'Dedicated video production team for product demos',
      priority: 'medium'
    },
    {
      id: 3,
      resourceName: 'Adobe Creative Suite',
      resourceType: 'software',
      allocatedTo: 'Design Team',
      project: 'Brand Refresh',
      campaign: 'Brand Update 2024',
      amount: 10,
      unit: 'licenses',
      startDate: '2024-01-15',
      endDate: '2024-12-31',
      status: 'in-use',
      utilization: 80,
      cost: 12000,
      budgetRemaining: 0,
      assignedBy: 'Lisa Wang',
      notes: 'Creative software licenses for brand refresh project',
      priority: 'high'
    },
    {
      id: 4,
      resourceName: 'Conference Booth Space',
      resourceType: 'venue',
      allocatedTo: 'Ahmed Hassan',
      project: 'Trade Show Presence',
      campaign: 'Industry Conference 2024',
      amount: 1,
      unit: 'booth',
      startDate: '2024-03-15',
      endDate: '2024-03-17',
      status: 'allocated',
      utilization: 0,
      cost: 8500,
      budgetRemaining: 8500,
      assignedBy: 'Sarah Johnson',
      notes: 'Premium booth space at industry conference',
      priority: 'medium'
    },
    {
      id: 5,
      resourceName: 'External PR Agency',
      resourceType: 'external',
      allocatedTo: 'Marketing Team',
      project: 'Product Launch PR',
      campaign: 'Summer 2024',
      amount: 25000,
      unit: 'USD',
      startDate: '2024-04-01',
      endDate: '2024-06-30',
      status: 'allocated',
      utilization: 0,
      cost: 25000,
      budgetRemaining: 25000,
      assignedBy: 'Mike Chen',
      notes: 'External PR support for major product launch',
      priority: 'critical'
    }
  ];

  const folders: Folder[] = [
    {
      id: 1,
      name: 'Campaign Assets',
      path: '/Campaign Assets',
      assetCount: 45,
      size: 125829120,
      createdBy: 'Sarah Johnson',
      createdAt: '2023-06-01',
      isShared: true,
      permissions: ['read', 'write', 'share']
    },
    {
      id: 2,
      name: 'Brand Assets',
      path: '/Brand Assets',
      assetCount: 23,
      size: 67108864,
      createdBy: 'Design Team',
      createdAt: '2023-01-15',
      isShared: true,
      permissions: ['read', 'write']
    },
    {
      id: 3,
      name: 'Product Content',
      path: '/Product Content',
      assetCount: 67,
      size: 234881024,
      createdBy: 'David Kim',
      createdAt: '2023-08-20',
      isShared: false,
      permissions: ['read', 'write', 'delete']
    },
    {
      id: 4,
      name: 'Email Templates',
      path: '/Email Templates',
      assetCount: 34,
      size: 15728640,
      createdBy: 'Ahmed Hassan',
      createdAt: '2023-09-10',
      isShared: true,
      permissions: ['read']
    }
  ];

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'image': return <FileImage className="h-4 w-4" />;
      case 'video': return <FileVideo className="h-4 w-4" />;
      case 'audio': return <FileAudio className="h-4 w-4" />;
      case 'document': return <FileText className="h-4 w-4" />;
      case 'template': return <Layers className="h-4 w-4" />;
      case 'brand-asset': return <Palette className="h-4 w-4" />;
      default: return <File className="h-4 w-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'archived': return 'bg-gray-100 text-gray-800';
      case 'expired': return 'bg-red-100 text-red-800';
      case 'allocated': return 'bg-blue-100 text-blue-800';
      case 'in-use': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-gray-100 text-gray-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'overdue': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getApprovalStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'not-required': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getResourceTypeIcon = (type: string) => {
    switch (type) {
      case 'budget': return <DollarSign className="h-4 w-4" />;
      case 'personnel': return <Users className="h-4 w-4" />;
      case 'equipment': return <Monitor className="h-4 w-4" />;
      case 'software': return <Cpu className="h-4 w-4" />;
      case 'venue': return <Building className="h-4 w-4" />;
      case 'external': return <ExternalLink className="h-4 w-4" />;
      default: return <Package className="h-4 w-4" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         asset.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         asset.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesType = filterType === 'all' || asset.type === filterType;
    const matchesCategory = filterCategory === 'all' || asset.category === filterCategory;
    const matchesStatus = filterStatus === 'all' || asset.status === filterStatus;
    const matchesFolder = selectedFolder === null || asset.folder === folders.find(f => f.id === selectedFolder)?.name;
    return matchesSearch && matchesType && matchesCategory && matchesStatus && matchesFolder;
  });

  const assetStats = {
    total: assets.length,
    totalSize: assets.reduce((sum, asset) => sum + asset.size, 0),
    totalDownloads: assets.reduce((sum, asset) => sum + asset.downloads, 0),
    totalViews: assets.reduce((sum, asset) => sum + asset.views, 0),
    pendingApproval: assets.filter(a => a.approvalStatus === 'pending').length
  };

  const allocationStats = {
    total: allocations.length,
    totalBudget: allocations.filter(a => a.resourceType === 'budget').reduce((sum, a) => sum + a.amount, 0),
    totalSpent: allocations.reduce((sum, a) => sum + a.cost, 0),
    avgUtilization: allocations.reduce((sum, a) => sum + a.utilization, 0) / allocations.length,
    activeAllocations: allocations.filter(a => a.status === 'in-use' || a.status === 'allocated').length
  };

  const UploadAssetDialog = () => (
    <Dialog open={isUploadDialogOpen} onOpenChange={setIsUploadDialogOpen}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Upload New Asset</DialogTitle>
          <DialogDescription>
            Add a new asset to your resource library.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <p className="text-lg font-medium mb-2">Drop files here or click to browse</p>
            <p className="text-sm text-muted-foreground">
              Supports: Images (PNG, JPG, SVG), Videos (MP4, MOV), Documents (PDF, DOC), Audio (MP3, WAV)
            </p>
            <Button className="mt-4">
              <Upload className="h-4 w-4 mr-2" />
              Choose Files
            </Button>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="assetName">Asset Name</Label>
              <Input id="assetName" placeholder="Enter asset name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="assetCategory">Category</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="campaign-assets">Campaign Assets</SelectItem>
                  <SelectItem value="brand-assets">Brand Assets</SelectItem>
                  <SelectItem value="product-content">Product Content</SelectItem>
                  <SelectItem value="email-templates">Email Templates</SelectItem>
                  <SelectItem value="social-media">Social Media</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="assetFolder">Folder</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select folder" />
                </SelectTrigger>
                <SelectContent>
                  {folders.map((folder) => (
                    <SelectItem key={folder.id} value={folder.name}>
                      {folder.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="assetLicense">License</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select license" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="internal">Internal Use</SelectItem>
                  <SelectItem value="commercial">Commercial</SelectItem>
                  <SelectItem value="creative-commons">Creative Commons</SelectItem>
                  <SelectItem value="royalty-free">Royalty Free</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="assetDescription">Description</Label>
            <Textarea id="assetDescription" placeholder="Describe the asset and its intended use" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="assetTags">Tags (comma-separated)</Label>
            <Input id="assetTags" placeholder="campaign, hero, banner, summer" />
          </div>

          <div className="flex items-center space-x-2">
            <Checkbox id="requiresApproval" />
            <Label htmlFor="requiresApproval">Requires approval before use</Label>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsUploadDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsUploadDialogOpen(false)}>
            Upload Asset
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  const CreateFolderDialog = () => (
    <Dialog open={isCreateFolderDialogOpen} onOpenChange={setIsCreateFolderDialogOpen}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Folder</DialogTitle>
          <DialogDescription>
            Organize your assets with a new folder.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="folderName">Folder Name</Label>
            <Input id="folderName" placeholder="Enter folder name" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="parentFolder">Parent Folder (Optional)</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select parent folder" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="root">Root Directory</SelectItem>
                {folders.map((folder) => (
                  <SelectItem key={folder.id} value={folder.name}>
                    {folder.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="folderDescription">Description</Label>
            <Textarea id="folderDescription" placeholder="Describe the folder's purpose" />
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox id="shareFolder" />
            <Label htmlFor="shareFolder">Share with team</Label>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsCreateFolderDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsCreateFolderDialogOpen(false)}>
            Create Folder
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  const AllocateResourceDialog = () => (
    <Dialog open={isAllocateResourceDialogOpen} onOpenChange={setIsAllocateResourceDialogOpen}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Allocate Resource</DialogTitle>
          <DialogDescription>
            Assign resources to projects and campaigns.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="resourceName">Resource Name</Label>
              <Input id="resourceName" placeholder="Enter resource name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="resourceType">Resource Type</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="budget">Budget</SelectItem>
                  <SelectItem value="personnel">Personnel</SelectItem>
                  <SelectItem value="equipment">Equipment</SelectItem>
                  <SelectItem value="software">Software</SelectItem>
                  <SelectItem value="venue">Venue</SelectItem>
                  <SelectItem value="external">External Service</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="allocatedTo">Allocated To</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select person/team" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="sarah">Sarah Johnson</SelectItem>
                  <SelectItem value="mike">Mike Chen</SelectItem>
                  <SelectItem value="david">David Kim</SelectItem>
                  <SelectItem value="emily">Emily Rodriguez</SelectItem>
                  <SelectItem value="marketing-team">Marketing Team</SelectItem>
                  <SelectItem value="design-team">Design Team</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="project">Project</Label>
              <Input id="project" placeholder="Enter project name" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="campaign">Campaign</Label>
              <Input id="campaign" placeholder="Enter campaign name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="priority">Priority</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="amount">Amount</Label>
              <Input id="amount" type="number" placeholder="Enter amount" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="unit">Unit</Label>
              <Input id="unit" placeholder="USD, people, hours" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="cost">Cost</Label>
              <Input id="cost" type="number" placeholder="Enter cost" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="startDate">Start Date</Label>
              <Input id="startDate" type="date" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="endDate">End Date</Label>
              <Input id="endDate" type="date" />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
            <Textarea id="notes" placeholder="Additional notes about the allocation" />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setIsAllocateResourceDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={() => setIsAllocateResourceDialogOpen(false)}>
            Allocate Resource
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <FolderOpen className="h-8 w-8 text-blue-600" />
            Resource Management
          </h1>
          <p className="text-muted-foreground">
            Manage marketing assets and resource allocation
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" onClick={() => setIsCreateFolderDialogOpen(true)}>
            <FolderPlus className="h-4 w-4 mr-2" />
            New Folder
          </Button>
          <Button onClick={() => setIsUploadDialogOpen(true)}>
            <Upload className="h-4 w-4 mr-2" />
            Upload Asset
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <File className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{assetStats.total}</div>
            <p className="text-xs text-muted-foreground">
              {formatFileSize(assetStats.totalSize)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Downloads</CardTitle>
            <Download className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{assetStats.totalDownloads}</div>
            <p className="text-xs text-muted-foreground">
              {assetStats.totalViews} views
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Budget Allocated</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${allocationStats.totalBudget.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              ${allocationStats.totalSpent.toLocaleString()} spent
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Utilization</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{allocationStats.avgUtilization.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Average utilization
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Approval</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{assetStats.pendingApproval}</div>
            <p className="text-xs text-muted-foreground">
              Assets pending
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="assets">Digital Assets</TabsTrigger>
          <TabsTrigger value="allocations">Resource Allocation</TabsTrigger>
          <TabsTrigger value="folders">Folder Management</TabsTrigger>
          <TabsTrigger value="analytics">Usage Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="assets" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Digital Asset Library</CardTitle>
                  <CardDescription>
                    Manage your marketing assets and digital resources
                  </CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant={viewMode === 'grid' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setViewMode('grid')}
                  >
                    <Grid className="h-4 w-4" />
                  </Button>
                  <Button
                    variant={viewMode === 'list' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setViewMode('list')}
                  >
                    <List className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4 mb-6">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="Search assets..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={filterType} onValueChange={setFilterType}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="image">Images</SelectItem>
                    <SelectItem value="video">Videos</SelectItem>
                    <SelectItem value="audio">Audio</SelectItem>
                    <SelectItem value="document">Documents</SelectItem>
                    <SelectItem value="template">Templates</SelectItem>
                    <SelectItem value="brand-asset">Brand Assets</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={filterCategory} onValueChange={setFilterCategory}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    <SelectItem value="Campaign Assets">Campaign Assets</SelectItem>
                    <SelectItem value="Brand Assets">Brand Assets</SelectItem>
                    <SelectItem value="Product Content">Product Content</SelectItem>
                    <SelectItem value="Email Templates">Email Templates</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="archived">Archived</SelectItem>
                    <SelectItem value="expired">Expired</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Folder Navigation */}
              <div className="flex items-center gap-2 mb-4 p-2 bg-gray-50 rounded-lg">
                <Button
                  variant={selectedFolder === null ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setSelectedFolder(null)}
                >
                  <Folder className="h-4 w-4 mr-1" />
                  All Assets
                </Button>
                {folders.map((folder) => (
                  <Button
                    key={folder.id}
                    variant={selectedFolder === folder.id ? 'default' : 'ghost'}
                    size="sm"
                    onClick={() => setSelectedFolder(folder.id)}
                  >
                    <FolderOpen className="h-4 w-4 mr-1" />
                    {folder.name} ({folder.assetCount})
                  </Button>
                ))}
              </div>

              {viewMode === 'grid' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {filteredAssets.map((asset) => (
                    <Card key={asset.id} className="group hover:shadow-md transition-shadow">
                      <CardContent className="p-4">
                        <div className="aspect-video bg-gray-100 rounded-lg mb-3 relative overflow-hidden">
                          {asset.thumbnail ? (
                            <img
                              src={asset.thumbnail}
                              alt={asset.name}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center">
                              {getTypeIcon(asset.type)}
                            </div>
                          )}
                          <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <Button variant="secondary" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                          </div>
                          <div className="absolute top-2 left-2">
                            <Badge className={getStatusColor(asset.status)}>
                              {asset.status}
                            </Badge>
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div className="flex items-start justify-between">
                            <h3 className="font-medium text-sm line-clamp-2">{asset.name}</h3>
                            <div className="flex items-center gap-1">
                              {getTypeIcon(asset.type)}
                            </div>
                          </div>
                          <div className="flex items-center justify-between text-xs text-muted-foreground">
                            <span>{asset.format}</span>
                            <span>{formatFileSize(asset.size)}</span>
                          </div>
                          <div className="flex items-center justify-between text-xs text-muted-foreground">
                            <span>{asset.downloads} downloads</span>
                            <span>{asset.views} views</span>
                          </div>
                          <div className="flex flex-wrap gap-1">
                            {asset.tags.slice(0, 2).map((tag, index) => (
                              <Badge key={index} variant="secondary" className="text-xs">
                                {tag}
                              </Badge>
                            ))}
                            {asset.tags.length > 2 && (
                              <Badge variant="secondary" className="text-xs">
                                +{asset.tags.length - 2}
                              </Badge>
                            )}
                          </div>
                          <div className="flex items-center justify-between pt-2">
                            <Badge className={getApprovalStatusColor(asset.approvalStatus)} variant="outline">
                              {asset.approvalStatus.replace('-', ' ')}
                            </Badge>
                            <div className="flex items-center gap-1">
                              <Button variant="ghost" size="sm">
                                <Download className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Share2 className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Edit className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              ) : (
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Asset</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Size</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Usage</TableHead>
                        <TableHead>Modified</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredAssets.map((asset) => (
                        <TableRow key={asset.id}>
                          <TableCell>
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 bg-gray-100 rounded flex items-center justify-center">
                                {getTypeIcon(asset.type)}
                              </div>
                              <div>
                                <div className="font-medium">{asset.name}</div>
                                <div className="text-sm text-muted-foreground">{asset.description}</div>
                                <div className="flex items-center gap-1 mt-1">
                                  {asset.tags.slice(0, 3).map((tag, index) => (
                                    <Badge key={index} variant="secondary" className="text-xs">
                                      {tag}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div className="text-sm font-medium">{asset.format}</div>
                              <div className="text-xs text-muted-foreground capitalize">{asset.type.replace('-', ' ')}</div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div className="text-sm">{formatFileSize(asset.size)}</div>
                              {asset.dimensions && (
                                <div className="text-xs text-muted-foreground">{asset.dimensions}</div>
                              )}
                              {asset.duration && (
                                <div className="text-xs text-muted-foreground">{asset.duration}</div>
                              )}
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <Badge className={getStatusColor(asset.status)}>
                                {asset.status}
                              </Badge>
                              <div className="text-xs">
                                <Badge className={getApprovalStatusColor(asset.approvalStatus)} variant="outline">
                                  {asset.approvalStatus.replace('-', ' ')}
                                </Badge>
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div className="text-sm">{asset.downloads} downloads</div>
                              <div className="text-xs text-muted-foreground">{asset.views} views</div>
                              <div className="text-xs text-muted-foreground">
                                {asset.usage.campaigns + asset.usage.emails + asset.usage.social + asset.usage.web} total uses
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div className="text-sm">{asset.lastModified}</div>
                              <div className="text-xs text-muted-foreground">by {asset.createdBy}</div>
                            </div>
                          </TableCell>
                          <TableCell className="text-right">
                            <div className="flex items-center justify-end gap-2">
                              <Button variant="ghost" size="sm">
                                <Eye className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Download className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Share2 className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button variant="ghost" size="sm" className="text-red-600">
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="allocations" className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Resource Allocation</CardTitle>
                  <CardDescription>
                    Track and manage resource assignments across projects
                  </CardDescription>
                </div>
                <Button onClick={() => setIsAllocateResourceDialogOpen(true)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Allocate Resource
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Resource</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Allocated To</TableHead>
                      <TableHead>Project/Campaign</TableHead>
                      <TableHead>Amount</TableHead>
                      <TableHead>Utilization</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {allocations.map((allocation) => (
                      <TableRow key={allocation.id}>
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-gray-100 rounded flex items-center justify-center">
                              {getResourceTypeIcon(allocation.resourceType)}
                            </div>
                            <div>
                              <div className="font-medium">{allocation.resourceName}</div>
                              <div className="text-sm text-muted-foreground">
                                {allocation.startDate} - {allocation.endDate}
                              </div>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="capitalize">
                            {allocation.resourceType.replace('-', ' ')}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">{allocation.allocatedTo}</div>
                            <div className="text-xs text-muted-foreground">
                              Assigned by {allocation.assignedBy}
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">{allocation.project}</div>
                            <div className="text-xs text-muted-foreground">{allocation.campaign}</div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">
                              {allocation.amount.toLocaleString()} {allocation.unit}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              ${allocation.cost.toLocaleString()} cost
                            </div>
                            {allocation.budgetRemaining > 0 && (
                              <div className="text-xs text-green-600">
                                ${allocation.budgetRemaining.toLocaleString()} remaining
                              </div>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <div className="text-sm font-medium">{allocation.utilization}%</div>
                            <Progress value={allocation.utilization} className="h-1 w-16" />
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-1">
                            <Badge className={getStatusColor(allocation.status)}>
                              {allocation.status.replace('-', ' ')}
                            </Badge>
                            <div className="text-xs">
                              <Badge 
                                variant="outline"
                                className={
                                  allocation.priority === 'critical' ? 'border-red-200 text-red-800' :
                                  allocation.priority === 'high' ? 'border-orange-200 text-orange-800' :
                                  allocation.priority === 'medium' ? 'border-yellow-200 text-yellow-800' :
                                  'border-gray-200 text-gray-800'
                                }
                              >
                                {allocation.priority}
                              </Badge>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell className="text-right">
                          <div className="flex items-center justify-end gap-2">
                            <Button variant="ghost" size="sm">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Settings className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm" className="text-red-600">
                              <XCircle className="h-4 w-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="folders" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Folder Management</CardTitle>
              <CardDescription>
                Organize and manage your asset folders
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {folders.map((folder) => (
                  <Card key={folder.id} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <FolderOpen className="h-5 w-5 text-blue-600" />
                          <h3 className="font-medium">{folder.name}</h3>
                        </div>
                        <div className="flex items-center gap-1">
                          <Button variant="ghost" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-red-600">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      <div className="space-y-2 text-sm text-muted-foreground">
                        <div className="flex justify-between">
                          <span>Assets:</span>
                          <span>{folder.assetCount}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Size:</span>
                          <span>{formatFileSize(folder.size)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Created:</span>
                          <span>{folder.createdAt}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Created by:</span>
                          <span>{folder.createdBy}</span>
                        </div>
                      </div>
                      <div className="flex items-center justify-between mt-4">
                        <div className="flex items-center gap-1">
                          {folder.isShared && (
                            <Badge variant="secondary" className="text-xs">
                              <Share2 className="h-3 w-3 mr-1" />
                              Shared
                            </Badge>
                          )}
                        </div>
                        <Button variant="outline" size="sm" onClick={() => setSelectedFolder(folder.id)}>
                          <Eye className="h-4 w-4 mr-1" />
                          View
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Asset Usage by Type</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {['image', 'video', 'document', 'template', 'brand-asset'].map((type) => {
                    const typeAssets = assets.filter(a => a.type === type);
                    const totalUsage = typeAssets.reduce((sum, a) => sum + a.usage.campaigns + a.usage.emails + a.usage.social + a.usage.web, 0);
                    const percentage = (typeAssets.length / assets.length) * 100;
                    
                    return (
                      <div key={type} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <div className="flex items-center gap-2">
                            {getTypeIcon(type)}
                            <span className="capitalize">{type.replace('-', ' ')}</span>
                          </div>
                          <span>{typeAssets.length} assets</span>
                        </div>
                        <Progress value={percentage} className="h-2" />
                        <div className="text-xs text-muted-foreground">
                          {totalUsage} total uses
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Resource Utilization</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {allocations.map((allocation) => (
                    <div key={allocation.id} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <div className="flex items-center gap-2">
                          {getResourceTypeIcon(allocation.resourceType)}
                          <span>{allocation.resourceName}</span>
                        </div>
                        <span>{allocation.utilization}%</span>
                      </div>
                      <Progress value={allocation.utilization} className="h-2" />
                      <div className="text-xs text-muted-foreground">
                        {allocation.allocatedTo} • {allocation.status}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      <UploadAssetDialog />
      <CreateFolderDialog />
      <AllocateResourceDialog />
    </div>
  );
}