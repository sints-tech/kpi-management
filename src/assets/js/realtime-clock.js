/**
 * Real-time Clock
 * Menampilkan waktu dan tanggal secara real-time di navbar
 */

'use strict';

(function() {
  function updateClock() {
    const now = new Date();
    
    // Format waktu (HH:MM:SS)
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    // Format tanggal (DD MMM YYYY)
    const days = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
    
    const dayName = days[now.getDay()];
    const day = String(now.getDate()).padStart(2, '0');
    const month = months[now.getMonth()];
    const year = now.getFullYear();
    const dateString = `${day} ${month} ${year}`;
    
    // Update elemen
    const clockTimeEl = document.getElementById('clock-time');
    const clockDateEl = document.getElementById('clock-date');
    
    if (clockTimeEl) {
      clockTimeEl.textContent = timeString;
    }
    
    if (clockDateEl) {
      clockDateEl.textContent = dateString;
    }
  }
  
  // Update clock saat DOM ready
  document.addEventListener('DOMContentLoaded', function() {
    // Update immediately
    updateClock();
    
    // Update every second
    setInterval(updateClock, 1000);
  });
})();


