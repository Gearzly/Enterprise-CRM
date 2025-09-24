import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { SalesRepDashboard } from './components/dashboards/SalesRepDashboard';
import { ManagerDashboard } from './components/dashboards/ManagerDashboard';
import { AdminDashboard } from './components/dashboards/AdminDashboard';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/auth/LoginPage';
import { SignupPage } from './pages/auth/SignupPage';
import { ForgotPasswordPage } from './pages/auth/ForgotPasswordPage';
import { DashboardPage } from './pages/DashboardPage';

// Sales Pages
import { ActivitiesPage } from './pages/sales/ActivitiesPage';
import { ContactsPage } from './pages/sales/ContactsPage';
import { LeadsPage } from './pages/sales/LeadsPage';
import { OpportunitiesPage } from './pages/sales/OpportunitiesPage';
import { QuotationsPage } from './pages/sales/QuotationsPage';
import { ReportsPage } from './pages/sales/ReportsPage';
import { TargetsPage } from './pages/sales/TargetsPage';

// Sales Create/Edit Pages
import { CreateLeadPage } from './pages/sales/CreateLeadPage';
import { CreateContactPage } from './pages/sales/CreateContactPage';
import { CreateOpportunityPage } from './pages/sales/CreateOpportunityPage';
import { CreateQuotationPage } from './pages/sales/CreateQuotationPage';

// Marketing Pages  
import { CampaignsPage } from './pages/marketing/CampaignsPage';
import { ContentPage } from './pages/marketing/ContentPage';
import { SegmentationPage } from './pages/marketing/SegmentationPage';
import { EventsPage } from './pages/marketing/EventsPage';
import { PartnersPage } from './pages/marketing/PartnersPage';
import { ResourcesPage } from './pages/marketing/ResourcesPage';
import { CDPPage } from './pages/marketing/CDPPage';
import { LeadsPage as MarketingLeadsPage } from './pages/marketing/LeadsPage';
import { EmailPage } from './pages/marketing/EmailPage';
import { AnalyticsPage } from './pages/marketing/AnalyticsPage';
import { SocialMediaPage } from './pages/marketing/SocialMediaPage';
import { AutomationPage } from './pages/marketing/AutomationPage';

// Marketing Create/Edit Pages
import { CreateCampaignPage } from './pages/marketing/CreateCampaignPage';
import { CreateEmailTemplatePage } from './pages/marketing/CreateEmailTemplatePage';

// Support Pages
import { TicketsPage } from './pages/support/TicketsPage';
import { KnowledgeBasePage } from './pages/support/KnowledgeBasePage';
import { LiveChatPage } from './pages/support/LiveChatPage';
import { FeedbackPage } from './pages/support/FeedbackPage';

// Support Create/Edit Pages
import { CreateTicketPage } from './pages/support/CreateTicketPage';
import { CreateKnowledgeArticlePage } from './pages/support/CreateKnowledgeArticlePage';

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedRole, setSelectedRole] = useState<string>('Admin'); // Default role set to Admin
  const [editId, setEditId] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleViewChange = (view: string, id?: string) => {
    setCurrentView(view);
    setEditId(id || null);
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
    setCurrentView('dashboard'); // Redirect directly to dashboard
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentView('dashboard');
  };

  // If not authenticated, show auth pages
  if (!isAuthenticated) {
    return (
      <Routes>
        <Route path="/auth/login" element={<LoginPage onLogin={handleLogin} />} />
        <Route path="/auth/signup" element={<SignupPage />} />
        <Route path="/auth/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="*" element={<Navigate to="/auth/login" replace />} />
      </Routes>
    );
  }

  const renderContent = () => {
    // Dashboard views
    if (currentView === 'dashboard') {
      switch (selectedRole) {
        case 'Sales Rep':
          return <SalesRepDashboard />;
        case 'Sales Manager':
          return <ManagerDashboard />;
        case 'Admin':
          return <AdminDashboard />;
        default:
          return <SalesRepDashboard />;
      }
    }

    // Module routing
    if (currentView.includes('/')) {
      const parts = currentView.split('/');
      const [module, submodule, action] = parts;
      
      // Handle edit routes with IDs
      if (action === 'edit' && editId) {
        switch (`${module}/${submodule}`) {
          case 'sales/leads':
            return <CreateLeadPage onBack={() => setCurrentView('sales/leads')} leadId={editId} isEdit={true} />;
          case 'sales/contacts':
            return <CreateContactPage onBack={() => setCurrentView('sales/contacts')} contactId={editId} isEdit={true} />;
          case 'sales/opportunities':
            return <CreateOpportunityPage onBack={() => setCurrentView('sales/opportunities')} opportunityId={editId} isEdit={true} />;
          case 'sales/quotations':
            return <CreateQuotationPage onBack={() => setCurrentView('sales/quotations')} quotationId={editId} isEdit={true} />;
          case 'marketing/campaigns':
            return <CreateCampaignPage onBack={() => setCurrentView('marketing/campaigns')} campaignId={editId} isEdit={true} />;
          case 'marketing/email':
            return <CreateEmailTemplatePage onBack={() => setCurrentView('marketing/email')} templateId={editId} isEdit={true} />;
          case 'support/tickets':
            return <CreateTicketPage onBack={() => setCurrentView('support/tickets')} ticketId={editId} isEdit={true} />;
          case 'support/knowledge-base':
            return <CreateKnowledgeArticlePage onBack={() => setCurrentView('support/knowledge-base')} articleId={editId} isEdit={true} />;
        }
      }
      
      // Dedicated Pages
      switch (currentView) {
        // Sales Pages
        case 'sales/activities':
          return <ActivitiesPage />;
        case 'sales/contacts':
          return <ContactsPage />;
        case 'sales/leads':
          return <LeadsPage onNavigate={handleViewChange} />;
        case 'sales/opportunities':
          return <OpportunitiesPage />;
        case 'sales/quotations':
          return <QuotationsPage />;
        case 'sales/reports':
          return <ReportsPage />;
        case 'sales/targets':
          return <TargetsPage />;
        
        // Sales Create/Edit Pages
        case 'sales/leads/create':
          return <CreateLeadPage onBack={() => setCurrentView('sales/leads')} />;
        case 'sales/contacts/create':
          return <CreateContactPage onBack={() => setCurrentView('sales/contacts')} />;
        case 'sales/opportunities/create':
          return <CreateOpportunityPage onBack={() => setCurrentView('sales/opportunities')} />;
        case 'sales/quotations/create':
          return <CreateQuotationPage onBack={() => setCurrentView('sales/quotations')} />;
        
        // Marketing Pages
        case 'marketing/campaigns':
          return <CampaignsPage />;
        case 'marketing/content':
          return <ContentPage />;
        case 'marketing/segmentation':
          return <SegmentationPage />;
        case 'marketing/events':
          return <EventsPage />;
        case 'marketing/partners':
          return <PartnersPage />;
        case 'marketing/resources':
          return <ResourcesPage />;
        case 'marketing/cdp':
          return <CDPPage />;
        case 'marketing/leads':
          return <MarketingLeadsPage />;
        case 'marketing/email':
          return <EmailPage />;
        case 'marketing/analytics':
          return <AnalyticsPage />;
        case 'marketing/social-media':
          return <SocialMediaPage />;
        case 'marketing/automation':
          return <AutomationPage />;
        
        // Marketing Create/Edit Pages
        case 'marketing/campaigns/create':
          return <CreateCampaignPage onBack={() => setCurrentView('marketing/campaigns')} />;
        case 'marketing/email/create':
          return <CreateEmailTemplatePage onBack={() => setCurrentView('marketing/email')} />;
        
        // Support Pages
        case 'support/tickets':
          return <TicketsPage />;
        case 'support/knowledge-base':
          return <KnowledgeBasePage />;
        case 'support/live-chat':
          return <LiveChatPage />;
        case 'support/feedback':
          return <FeedbackPage />;
        
        // Support Create/Edit Pages
        case 'support/tickets/create':
          return <CreateTicketPage onBack={() => setCurrentView('support/tickets')} />;
        case 'support/knowledge-base/create':
          return <CreateKnowledgeArticlePage onBack={() => setCurrentView('support/knowledge-base')} />;
      }

      // Fallback to placeholder pages for modules not yet implemented
      const moduleConfigs = {
        // Marketing submodules (remaining ones not implemented)
        'marketing/content': { title: 'Content Management', description: 'Create and manage marketing content and assets' },
        'marketing/segmentation': { title: 'Customer Segmentation', description: 'Segment customers for targeted marketing' },
        'marketing/events': { title: 'Event Management', description: 'Plan and manage marketing events and webinars' },
        'marketing/partners': { title: 'Partner Management', description: 'Manage marketing partnerships and collaborations' },
        'marketing/resources': { title: 'Marketing Resources', description: 'Manage marketing assets and resource library' },
        'marketing/cdp': { title: 'Customer Data Platform', description: 'Unified customer data and insights platform' },
        
        // Support submodules (remaining ones not implemented)
        'support/interactions': { title: 'Customer Interactions', description: 'Track all customer support interactions' },
        'support/call-center': { title: 'Call Center', description: 'Manage inbound and outbound support calls' },
        'support/social-support': { title: 'Social Support', description: 'Manage customer support via social media' },
        'support/sla': { title: 'Service Level Agreements', description: 'Manage and track SLA compliance' },
        'support/asset': { title: 'Asset Management', description: 'Track customer assets and equipment' },
        'support/remote': { title: 'Remote Support', description: 'Provide remote assistance and support' },
        'support/community': { title: 'Community Support', description: 'Manage community forums and user groups' },
        'support/reporting': { title: 'Support Reporting', description: 'Generate support analytics and reports' },
        'support/automation': { title: 'Support Automation', description: 'Automate support workflows and responses' },
        'support/mobile': { title: 'Mobile Support', description: 'Mobile support app and functionality' },
        'support/integration': { title: 'Support Integrations', description: 'Integrate with external support tools' },
        'support/language': { title: 'Multi-language Support', description: 'Manage multi-language support options' },
      };

      const config = moduleConfigs[currentView as keyof typeof moduleConfigs];
      if (config) {
        return (
          <PlaceholderPage
            title={config.title}
            description={config.description}
            module={module}
            submodule={submodule}
          />
        );
      }
    }

    // Admin pages
    switch (currentView) {
      case 'users':
        return (
          <PlaceholderPage
            title="User Management"
            description="Manage system users, roles, and permissions"
            module="admin"
            submodule="users"
          />
        );
      case 'settings':
        return (
          <PlaceholderPage
            title="System Settings"
            description="Configure system settings and preferences"
            module="admin"
            submodule="settings"
          />
        );
      default:
        return <SalesRepDashboard />;
    }
  };

  return (
    <div className="flex h-screen bg-background">
      <Sidebar 
        currentView={currentView} 
        onViewChange={handleViewChange}
        userRole={selectedRole}
      />
      <main className="flex-1 overflow-auto">
        {renderContent()}
      </main>
    </div>
  );
}