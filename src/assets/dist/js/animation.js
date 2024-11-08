const appearElements = document.querySelectorAll(".scroll-animate");
const cb3 = function (entries, observer) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("inview");
      observer.unobserve(entry.target);
    }
  });
};
const io3 = new IntersectionObserver(cb3);
appearElements.forEach((element) => io3.observe(element));
