const page = getPathAsArray(window.location.pathname);
const navLinks = Array.from(document.querySelectorAll('.nav-link'));

const possibleMatches = ["admin", "scout"]

for (match of possibleMatches) {
  if (page.includes(match)){
    navLinks.forEach(nav => {
      if (nav.dataset.link === match)
        nav.classList.add('active');
    })
  }
}

if (page.length === 0) {
  navLinks.filter(nav => nav.dataset.link === "index")[0].classList.add('active');
}

function getPathAsArray(path) {
  const segments = path.split('/');
  
  return segments.filter(segment => segment.length); // Get rid of empty segments
}