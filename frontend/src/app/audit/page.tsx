'use client';
import AuditDashboard from '@/components/audit/AuditDashboard';
import SaudiRTLWrapper from '@/components/common/SaudiRTLWrapper';

export default function AuditPage() {
  return (
    <SaudiRTLWrapper>
      <AuditDashboard providerId="EXT-123" />
    </SaudiRTLWrapper>
  );
}
