import { useState } from 'react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Avatar, AvatarFallback, AvatarImage } from '../../components/ui/avatar';
import { Users, Plus, Filter, Search, Mail, Phone, Building, Star } from 'lucide-react';

export function ContactsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');

  const contacts = [
    {
      id: 1,
      name: 'John Smith',
      email: 'john.smith@acmecorp.com',
      phone: '+1 (555) 123-4567',
      company: 'Acme Corporation',
      position: 'CEO',
      type: 'customer',
      rating: 5,
      lastContact: '2024-01-15',
      value: '$125,000'
    },
    {
      id: 2,
      name: 'Sarah Johnson',
      email: 'sarah.j@techstart.com',
      phone: '+1 (555) 234-5678',
      company: 'TechStart Inc',
      position: 'CTO',
      type: 'lead',
      rating: 4,
      lastContact: '2024-01-14',
      value: '$85,000'
    },
    {
      id: 3,
      name: 'Mike Wilson',
      email: 'mike.wilson@globalsol.com',
      phone: '+1 (555) 345-6789',
      company: 'Global Solutions',
      position: 'VP Sales',
      type: 'prospect',
      rating: 3,
      lastContact: '2024-01-13',
      value: '$45,000'
    },
    {
      id: 4,
      name: 'Lisa Chen',
      email: 'lisa.chen@innovateco.com',
      phone: '+1 (555) 456-7890',
      company: 'InnovateCo',
      position: 'Director',
      type: 'customer',
      rating: 5,
      lastContact: '2024-01-12',
      value: '$95,000'
    }
  ];

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'customer': return 'bg-green-100 text-green-800';
      case 'lead': return 'bg-blue-100 text-blue-800';
      case 'prospect': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderRating = (rating: number) => {
    return (
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`w-4 h-4 ${
              star <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
            }`}
          />
        ))}
      </div>
    );
  };

  const filteredContacts = contacts.filter(contact => {
    const matchesSearch = contact.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         contact.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         contact.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || contact.type === filterType;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Contacts Management</h1>
          <p className="text-muted-foreground">Manage customer contacts and relationships</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Import Contacts</Button>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Add Contact
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Total Contacts</p>
              <p className="text-xl font-semibold">1,247</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <Building className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Companies</p>
              <p className="text-xl font-semibold">423</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Star className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">5-Star Contacts</p>
              <p className="text-xl font-semibold">89</p>
            </div>
          </div>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Mail className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Active This Week</p>
              <p className="text-xl font-semibold">156</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Filters and Search */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search contacts..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={filterType} onValueChange={setFilterType}>
          <SelectTrigger className="w-[200px]">
            <Filter className="w-4 h-4 mr-2" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="customer">Customers</SelectItem>
            <SelectItem value="lead">Leads</SelectItem>
            <SelectItem value="prospect">Prospects</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Contacts Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Contact</TableHead>
              <TableHead>Company & Position</TableHead>
              <TableHead>Contact Info</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Rating</TableHead>
              <TableHead>Last Contact</TableHead>
              <TableHead>Value</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredContacts.map((contact) => (
              <TableRow key={contact.id}>
                <TableCell>
                  <div className="flex items-center gap-3">
                    <Avatar>
                      <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${contact.name}`} />
                      <AvatarFallback>{contact.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <div>
                      <div className="font-medium">{contact.name}</div>
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <div>
                    <div className="font-medium">{contact.company}</div>
                    <div className="text-sm text-muted-foreground">{contact.position}</div>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 text-sm">
                      <Mail className="w-3 h-3" />
                      {contact.email}
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Phone className="w-3 h-3" />
                      {contact.phone}
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge className={getTypeColor(contact.type)}>
                    {contact.type}
                  </Badge>
                </TableCell>
                <TableCell>{renderRating(contact.rating)}</TableCell>
                <TableCell>{contact.lastContact}</TableCell>
                <TableCell className="font-medium">{contact.value}</TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Edit</Button>
                    <Button variant="outline" size="sm">View</Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
}