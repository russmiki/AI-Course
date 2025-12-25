/**
 * Error handler utility for converting error objects to Persian error messages
 * @param {Error} error - The error object to process
 * @returns {string} - Persian error message
 */
export function getErrorMessage(error) {
  if (error.message?.includes("network") || error.message?.includes("fetch")) {
    return "خطا در اتصال به اینترنت. لطفاً اتصال خود را بررسی کنید.";
  }
  if (error.message?.includes("API") || error.message?.includes("apiKey")) {
    return "خطا در احراز هویت. لطفاً کلید API را بررسی کنید.";
  }
  if (error.message?.includes("quota") || error.message?.includes("limit")) {
    return "محدودیت استفاده از سرویس. لطفاً بعداً تلاش کنید.";
  }
  if (error.message?.includes("timeout")) {
    return "زمان درخواست به پایان رسید. لطفاً دوباره تلاش کنید.";
  }
  return "خطایی در دریافت پاسخ رخ داد. لطفاً دوباره تلاش کنید.";
}
