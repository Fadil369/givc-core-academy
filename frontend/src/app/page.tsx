import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-midnight via-primary-medical to-primary-signal">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h1 className="text-5xl font-bold mb-6 font-arabic">
            أكاديمية GIVC الأساسية
          </h1>
          <h2 className="text-4xl font-bold mb-4">
            GIVC Core Academy
          </h2>
          <p className="text-xl mb-8 font-arabic">
            منصة تدريب شاملة للتأمين الصحي والترميز الطبي في المملكة العربية السعودية
          </p>
          <p className="text-lg mb-12">
            Comprehensive healthcare insurance and medical coding training for Saudi Arabia
          </p>
          
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white/10 backdrop-blur-md rounded-lg p-6">
              <h3 className="text-2xl font-bold mb-2">ICD-10-AM</h3>
              <p className="font-arabic">التصنيف الدولي للأمراض</p>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-lg p-6">
              <h3 className="text-2xl font-bold mb-2">SBS</h3>
              <p className="font-arabic">نظام الفوترة السعودي</p>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-lg p-6">
              <h3 className="text-2xl font-bold mb-2">AR-DRG</h3>
              <p className="font-arabic">مجموعات التشخيص العربية</p>
            </div>
          </div>

          <div className="flex flex-wrap gap-4 justify-center">
             <Link
              href="/audit"
              className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              <span className="font-arabic">لوحة التدقيق</span> / Audit Dashboard
            </Link>
             <Link
              href="/learning"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition"
            >
              <span className="font-arabic">بوابة التعلم</span> / Learning Portal
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
