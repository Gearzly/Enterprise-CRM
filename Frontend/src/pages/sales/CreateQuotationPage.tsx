import { useState } from 'react';
import { ArrowLeft, Save, FileText, Calculator, Plus, X } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { Textarea } from '../../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';

interface QuoteItem {
  id: string;
  product: string;
  description: string;
  quantity: number;
  unitPrice: number;
  discount: number;
  total: number;
}

interface CreateQuotationPageProps {
  onBack?: () => void;
  quotationId?: string;
  isEdit?: boolean;
}

export function CreateQuotationPage({ onBack, quotationId, isEdit = false }: CreateQuotationPageProps) {
  const [formData, setFormData] = useState({
    quoteNumber: '',
    customer: '',
    opportunity: '',
    contact: '',
    validUntil: '',
    paymentTerms: '',
    deliveryTerms: '',
    currency: 'USD',
    taxRate: '10',
    discountType: 'percentage',
    discountValue: '',
    shippingCost: '',
    notes: '',
    terms: '',
    status: 'draft',
    assignedTo: ''
  });

  const [items, setItems] = useState<QuoteItem[]>([
    {
      id: '1',
      product: '',
      description: '',
      quantity: 1,
      unitPrice: 0,
      discount: 0,
      total: 0
    }
  ]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Quotation data:', { formData, items });
    if (onBack) onBack();
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const addItem = () => {
    const newItem: QuoteItem = {
      id: Date.now().toString(),
      product: '',
      description: '',
      quantity: 1,
      unitPrice: 0,
      discount: 0,
      total: 0
    };
    setItems([...items, newItem]);
  };

  const removeItem = (id: string) => {
    setItems(items.filter(item => item.id !== id));
  };

  const updateItem = (id: string, field: keyof QuoteItem, value: string | number) => {
    setItems(items.map(item => {
      if (item.id === id) {
        const updatedItem = { ...item, [field]: value };
        // Recalculate total
        const subtotal = updatedItem.quantity * updatedItem.unitPrice;
        const discountAmount = (subtotal * updatedItem.discount) / 100;
        updatedItem.total = subtotal - discountAmount;
        return updatedItem;
      }
      return item;
    }));
  };

  const calculateSubtotal = () => {
    return items.reduce((sum, item) => sum + item.total, 0);
  };

  const calculateDiscount = () => {
    const subtotal = calculateSubtotal();
    const discountValue = parseFloat(formData.discountValue) || 0;
    if (formData.discountType === 'percentage') {
      return (subtotal * discountValue) / 100;
    }
    return discountValue;
  };

  const calculateTax = () => {
    const subtotal = calculateSubtotal() - calculateDiscount();
    const taxRate = parseFloat(formData.taxRate) || 0;
    return (subtotal * taxRate) / 100;
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    const discount = calculateDiscount();
    const tax = calculateTax();
    const shipping = parseFloat(formData.shippingCost) || 0;
    return subtotal - discount + tax + shipping;
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={onBack}
          className="p-2"
        >
          <ArrowLeft className="w-4 h-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-medium">{isEdit ? 'Edit Quotation' : 'Create New Quotation'}</h1>
          <p className="text-muted-foreground">
            {isEdit ? 'Update quotation information' : 'Generate a new sales quotation'}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <FileText className="w-5 h-5" />
            <CardTitle>Quote Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="quoteNumber">Quote Number *</Label>
                <Input
                  id="quoteNumber"
                  value={formData.quoteNumber}
                  onChange={(e) => handleInputChange('quoteNumber', e.target.value)}
                  placeholder="Q-2024-001"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="validUntil">Valid Until *</Label>
                <Input
                  id="validUntil"
                  type="date"
                  value={formData.validUntil}
                  onChange={(e) => handleInputChange('validUntil', e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select value={formData.status} onValueChange={(value) => handleInputChange('status', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="draft">Draft</SelectItem>
                    <SelectItem value="sent">Sent</SelectItem>
                    <SelectItem value="accepted">Accepted</SelectItem>
                    <SelectItem value="rejected">Rejected</SelectItem>
                    <SelectItem value="expired">Expired</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="customer">Customer *</Label>
                <Select value={formData.customer} onValueChange={(value) => handleInputChange('customer', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select customer" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="acme-corp">Acme Corporation</SelectItem>
                    <SelectItem value="globex">Globex Industries</SelectItem>
                    <SelectItem value="initech">Initech Solutions</SelectItem>
                    <SelectItem value="umbrella">Umbrella Corp</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="opportunity">Related Opportunity</Label>
                <Select value={formData.opportunity} onValueChange={(value) => handleInputChange('opportunity', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select opportunity" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="opp-1">Acme Corp - Software License</SelectItem>
                    <SelectItem value="opp-2">Globex - Consulting Services</SelectItem>
                    <SelectItem value="opp-3">Initech - System Integration</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="contact">Primary Contact</Label>
                <Select value={formData.contact} onValueChange={(value) => handleInputChange('contact', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select contact" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="john-smith">John Smith</SelectItem>
                    <SelectItem value="jane-doe">Jane Doe</SelectItem>
                    <SelectItem value="mike-johnson">Mike Johnson</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quote Items */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <Calculator className="w-5 h-5" />
              <CardTitle>Quote Items</CardTitle>
            </div>
            <Button type="button" variant="outline" size="sm" onClick={addItem}>
              <Plus className="w-4 h-4 mr-2" />
              Add Item
            </Button>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product/Service</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead className="w-20">Qty</TableHead>
                  <TableHead className="w-24">Unit Price</TableHead>
                  <TableHead className="w-20">Discount %</TableHead>
                  <TableHead className="w-24">Total</TableHead>
                  <TableHead className="w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {items.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <Input
                        value={item.product}
                        onChange={(e) => updateItem(item.id, 'product', e.target.value)}
                        placeholder="Product name"
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        value={item.description}
                        onChange={(e) => updateItem(item.id, 'description', e.target.value)}
                        placeholder="Description"
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        type="number"
                        min="1"
                        value={item.quantity}
                        onChange={(e) => updateItem(item.id, 'quantity', parseInt(e.target.value) || 1)}
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        type="number"
                        min="0"
                        step="0.01"
                        value={item.unitPrice}
                        onChange={(e) => updateItem(item.id, 'unitPrice', parseFloat(e.target.value) || 0)}
                      />
                    </TableCell>
                    <TableCell>
                      <Input
                        type="number"
                        min="0"
                        max="100"
                        value={item.discount}
                        onChange={(e) => updateItem(item.id, 'discount', parseFloat(e.target.value) || 0)}
                      />
                    </TableCell>
                    <TableCell>
                      <span className="font-medium">${item.total.toFixed(2)}</span>
                    </TableCell>
                    <TableCell>
                      {items.length > 1 && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => removeItem(item.id)}
                        >
                          <X className="w-4 h-4" />
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Pricing & Terms */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Pricing Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="currency">Currency</Label>
                  <Select value={formData.currency} onValueChange={(value) => handleInputChange('currency', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select currency" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="USD">USD ($)</SelectItem>
                      <SelectItem value="EUR">EUR (€)</SelectItem>
                      <SelectItem value="GBP">GBP (£)</SelectItem>
                      <SelectItem value="CAD">CAD (C$)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="taxRate">Tax Rate (%)</Label>
                  <Input
                    id="taxRate"
                    type="number"
                    min="0"
                    max="100"
                    step="0.01"
                    value={formData.taxRate}
                    onChange={(e) => handleInputChange('taxRate', e.target.value)}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="discountType">Discount Type</Label>
                  <Select value={formData.discountType} onValueChange={(value) => handleInputChange('discountType', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="percentage">Percentage (%)</SelectItem>
                      <SelectItem value="fixed">Fixed Amount</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="discountValue">Discount Value</Label>
                  <Input
                    id="discountValue"
                    type="number"
                    min="0"
                    step="0.01"
                    value={formData.discountValue}
                    onChange={(e) => handleInputChange('discountValue', e.target.value)}
                    placeholder={formData.discountType === 'percentage' ? '0.00' : '0.00'}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="shippingCost">Shipping Cost</Label>
                <Input
                  id="shippingCost"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.shippingCost}
                  onChange={(e) => handleInputChange('shippingCost', e.target.value)}
                  placeholder="0.00"
                />
              </div>

              {/* Quote Summary */}
              <div className="border-t pt-4 space-y-2">
                <div className="flex justify-between">
                  <span>Subtotal:</span>
                  <span>${calculateSubtotal().toFixed(2)}</span>
                </div>
                {parseFloat(formData.discountValue) > 0 && (
                  <div className="flex justify-between text-red-600">
                    <span>Discount:</span>
                    <span>-${calculateDiscount().toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span>Tax:</span>
                  <span>${calculateTax().toFixed(2)}</span>
                </div>
                {parseFloat(formData.shippingCost) > 0 && (
                  <div className="flex justify-between">
                    <span>Shipping:</span>
                    <span>${parseFloat(formData.shippingCost).toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between font-semibold text-lg border-t pt-2">
                  <span>Total:</span>
                  <span>${calculateTotal().toFixed(2)}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Terms & Conditions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="paymentTerms">Payment Terms</Label>
                <Select value={formData.paymentTerms} onValueChange={(value) => handleInputChange('paymentTerms', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select payment terms" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="net-30">Net 30 days</SelectItem>
                    <SelectItem value="net-15">Net 15 days</SelectItem>
                    <SelectItem value="net-7">Net 7 days</SelectItem>
                    <SelectItem value="due-on-receipt">Due on receipt</SelectItem>
                    <SelectItem value="50-50">50% upfront, 50% on delivery</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="deliveryTerms">Delivery Terms</Label>
                <Select value={formData.deliveryTerms} onValueChange={(value) => handleInputChange('deliveryTerms', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select delivery terms" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="immediate">Immediate delivery</SelectItem>
                    <SelectItem value="1-week">Within 1 week</SelectItem>
                    <SelectItem value="2-weeks">Within 2 weeks</SelectItem>
                    <SelectItem value="1-month">Within 1 month</SelectItem>
                    <SelectItem value="custom">Custom timeline</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="assignedTo">Assigned To</Label>
                <Select value={formData.assignedTo} onValueChange={(value) => handleInputChange('assignedTo', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select sales rep" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="john-doe">John Doe</SelectItem>
                    <SelectItem value="jane-smith">Jane Smith</SelectItem>
                    <SelectItem value="mike-johnson">Mike Johnson</SelectItem>
                    <SelectItem value="sarah-wilson">Sarah Wilson</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="terms">Terms & Conditions</Label>
                <Textarea
                  id="terms"
                  value={formData.terms}
                  onChange={(e) => handleInputChange('terms', e.target.value)}
                  placeholder="Enter terms and conditions..."
                  rows={4}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="notes">Internal Notes</Label>
                <Textarea
                  id="notes"
                  value={formData.notes}
                  onChange={(e) => handleInputChange('notes', e.target.value)}
                  placeholder="Internal notes about this quote..."
                  rows={3}
                />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Form Actions */}
        <div className="flex items-center justify-end gap-4 pt-6">
          <Button type="button" variant="outline" onClick={onBack}>
            Cancel
          </Button>
          <Button type="submit" className="min-w-[120px]">
            <Save className="w-4 h-4 mr-2" />
            {isEdit ? 'Update Quote' : 'Create Quote'}
          </Button>
        </div>
      </form>
    </div>
  );
}