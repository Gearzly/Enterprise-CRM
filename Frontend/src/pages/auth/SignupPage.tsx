import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Link } from 'react-router-dom';

export function SignupPage() {
  // User fields
  const [firstName, setFirstName] = React.useState('');
  const [lastName, setLastName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirmPassword, setConfirmPassword] = React.useState('');
  
  // Organization fields
  const [organizationName, setOrganizationName] = React.useState('');
  const [organizationDomain, setOrganizationDomain] = React.useState('');
  const [planType, setPlanType] = React.useState('basic');
  const [maxUsers, setMaxUsers] = React.useState('10');

  // Form validation state
  const [errors, setErrors] = React.useState<{[key: string]: string}>({});
  const [isLoading, setIsLoading] = React.useState(false);
  const [submitMessage, setSubmitMessage] = React.useState<{type: 'success' | 'error', text: string} | null>(null);

  // Validation functions
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password: string): string[] => {
    const errors: string[] = [];
    if (password.length < 8) errors.push('Password must be at least 8 characters long');
    if (!/[A-Z]/.test(password)) errors.push('Password must contain at least one uppercase letter');
    if (!/[a-z]/.test(password)) errors.push('Password must contain at least one lowercase letter');
    if (!/\d/.test(password)) errors.push('Password must contain at least one number');
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) errors.push('Password must contain at least one special character');
    return errors;
  };

  const validateForm = (): boolean => {
    const newErrors: {[key: string]: string} = {};

    // Personal Information Validation
    if (!firstName.trim()) newErrors.firstName = 'First name is required';
    if (!lastName.trim()) newErrors.lastName = 'Last name is required';
    
    if (!email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    } else {
      const passwordErrors = validatePassword(password);
      if (passwordErrors.length > 0) {
        newErrors.password = passwordErrors[0]; // Show first error
      }
    }

    if (!confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Organization Information Validation
    if (!organizationName.trim()) {
      newErrors.organizationName = 'Organization name is required';
    }

    if (organizationDomain && !/^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.[a-zA-Z]{2,}$/.test(organizationDomain)) {
      newErrors.organizationDomain = 'Please enter a valid domain (e.g., company.com)';
    }

    if (!planType) {
      newErrors.planType = 'Please select a plan type';
    }

    if (!maxUsers) {
      newErrors.maxUsers = 'Please select maximum users';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Clear previous messages
    setSubmitMessage(null);
    
    // Validate form
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Create signup data structure matching backend models
      const signupData = {
        user: {
          email: email.trim().toLowerCase(),
          first_name: firstName.trim(),
          last_name: lastName.trim(),
          password,
          status: 'active'
        },
        organization: {
          name: organizationName.trim(),
          domain: organizationDomain ? organizationDomain.trim().toLowerCase() : null,
          admin_email: email.trim().toLowerCase(),
          admin_password: password,
          status: 'active',
          plan_type: planType,
          max_users: parseInt(maxUsers),
          features: planType === 'basic' ? ['sales'] : 
                   planType === 'professional' ? ['sales', 'marketing'] : 
                   ['sales', 'marketing', 'support']
        }
      };

      console.log('Signup data prepared:', signupData);
      
      // TODO: Replace with actual API call when backend endpoint is ready
      // const response = await fetch('/api/signup', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(signupData),
      // });
      
      // if (!response.ok) {
      //   throw new Error('Signup failed');
      // }
      
      // const result = await response.json();
      
      // Simulate API call for now
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setSubmitMessage({
        type: 'success',
        text: 'Account created successfully! Please check your email for verification.'
      });
      
      // Reset form after successful submission
      setTimeout(() => {
        setFirstName('');
        setLastName('');
        setEmail('');
        setPassword('');
        setConfirmPassword('');
        setOrganizationName('');
        setOrganizationDomain('');
        setPlanType('basic');
        setMaxUsers('10');
        setSubmitMessage(null);
      }, 3000);
      
    } catch (error) {
      console.error('Signup error:', error);
      setSubmitMessage({
        type: 'error',
        text: 'Failed to create account. Please try again.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Card className="w-full max-w-2xl">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">Create an account</CardTitle>
          <CardDescription className="text-center">
            Enter your information to create your account and organization
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6">
            {/* Personal Information Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Personal Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    type="text"
                    placeholder="John"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                    className={errors.firstName ? 'border-red-500' : ''}
                  />
                  {errors.firstName && <p className="text-sm text-red-500">{errors.firstName}</p>}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    type="text"
                    placeholder="Doe"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                    className={errors.lastName ? 'border-red-500' : ''}
                  />
                  {errors.lastName && <p className="text-sm text-red-500">{errors.lastName}</p>}
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="john.doe@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className={errors.email ? 'border-red-500' : ''}
                />
                {errors.email && <p className="text-sm text-red-500">{errors.email}</p>}
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Minimum 8 characters"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={8}
                    className={errors.password ? 'border-red-500' : ''}
                  />
                  {errors.password && <p className="text-sm text-red-500">{errors.password}</p>}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    placeholder="Confirm your password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                    minLength={8}
                    className={errors.confirmPassword ? 'border-red-500' : ''}
                  />
                  {errors.confirmPassword && <p className="text-sm text-red-500">{errors.confirmPassword}</p>}
                </div>
              </div>
            </div>

            {/* Organization Information Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Organization Information</h3>
              <div className="space-y-2">
                <Label htmlFor="organizationName">Organization Name</Label>
                <Input
                  id="organizationName"
                  type="text"
                  placeholder="Your Company Name"
                  value={organizationName}
                  onChange={(e) => setOrganizationName(e.target.value)}
                  required
                  className={errors.organizationName ? 'border-red-500' : ''}
                />
                {errors.organizationName && <p className="text-sm text-red-500">{errors.organizationName}</p>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="organizationDomain">Organization Domain (Optional)</Label>
                <Input
                  id="organizationDomain"
                  type="text"
                  placeholder="company.com"
                  value={organizationDomain}
                  onChange={(e) => setOrganizationDomain(e.target.value)}
                  className={errors.organizationDomain ? 'border-red-500' : ''}
                />
                {errors.organizationDomain && <p className="text-sm text-red-500">{errors.organizationDomain}</p>}
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="planType">Plan Type</Label>
                  <Select value={planType} onValueChange={setPlanType}>
                    <SelectTrigger className={errors.planType ? 'border-red-500' : ''}>
                      <SelectValue placeholder="Select a plan" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="basic">Basic (Sales only)</SelectItem>
                      <SelectItem value="professional">Professional (Sales + Marketing)</SelectItem>
                      <SelectItem value="enterprise">Enterprise (All modules)</SelectItem>
                    </SelectContent>
                  </Select>
                  {errors.planType && <p className="text-sm text-red-500">{errors.planType}</p>}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="maxUsers">Maximum Users</Label>
                  <Select value={maxUsers} onValueChange={setMaxUsers}>
                    <SelectTrigger className={errors.maxUsers ? 'border-red-500' : ''}>
                      <SelectValue placeholder="Select user limit" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="5">5 Users</SelectItem>
                      <SelectItem value="10">10 Users</SelectItem>
                      <SelectItem value="25">25 Users</SelectItem>
                      <SelectItem value="50">50 Users</SelectItem>
                      <SelectItem value="100">100 Users</SelectItem>
                      <SelectItem value="250">250 Users</SelectItem>
                      <SelectItem value="500">500 Users</SelectItem>
                    </SelectContent>
                  </Select>
                  {errors.maxUsers && <p className="text-sm text-red-500">{errors.maxUsers}</p>}
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            {submitMessage && (
              <div className={`p-3 rounded-md text-sm ${
                submitMessage.type === 'success' 
                  ? 'bg-green-50 text-green-700 border border-green-200' 
                  : 'bg-red-50 text-red-700 border border-red-200'
              }`}>
                {submitMessage.text}
              </div>
            )}
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Creating Account...
                </>
              ) : (
                'Create Account & Organization'
              )}
            </Button>
            <div className="text-sm text-center">
              Already have an account?{' '}
              <Link to="/auth/login" className="font-medium text-blue-600 hover:underline">
                Sign in
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}