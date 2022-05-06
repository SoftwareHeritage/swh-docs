$(document).ready(function () {
  // open external link in new browser tab
  $('a.external:not([href^="https://docs.softwareheritage.org/"])')
    .attr('target', '_blank')
    .attr('rel', 'noopener noreferrer');
});
