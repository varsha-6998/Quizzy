document.getElementById('registrationForm').addEventListener('submit', function(e) {
      e.preventDefault();
      
      
      const formData = new FormData(this);
      const data = {};
      
      
      for (let [key, value] of formData.entries()) {
        if (data[key]) {
          if (Array.isArray(data[key])) {
            data[key].push(value);
          } else {
            data[key] = [data[key], value];
          }
        } else {
          data[key] = value;
        }
      }
      
      
      if (data.password !== data.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }
      
      if (!data.agreeTerms) {
        alert('Please agree to the Terms & Conditions');
        return;
      }
      
      
      const submitBtn = document.querySelector('.submit-btn');
      submitBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
      submitBtn.textContent = 'Registration Successful!';
      
      setTimeout(() => {
        submitBtn.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
        submitBtn.textContent = 'Register';
      }, 2000);
      
      console.log('Registration data:', data);
    });

    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
        });
      });
    });

    
    document.querySelectorAll('.form-input').forEach(input => {
      input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
      });
      
      input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
      });
    });