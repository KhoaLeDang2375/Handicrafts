import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// Tạo đường dẫn tuyệt đối tới file _variables.scss
const variablePath = resolve(process.cwd(), 'src/scss/abstract/_variables.scss');

// Đổi tất cả dấu \ (của Windows) thành / (mà SASS hiểu)
const normalizedPath = variablePath.replace(/\\/g, '/');

export default defineConfig({
  plugins: [react()],
  
  css: {
    preprocessorOptions: {
      scss: {
        // Tiêm đường dẫn đã được chuẩn hóa
        additionalData: `@use "${normalizedPath}" as *;\n`
      }
    }
  }
});