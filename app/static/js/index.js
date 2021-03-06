async function fetchTBA(endpoint) {
  if (endpoint[0] == '/')
    endpoint = endpoint.substring(1);

  const config = {
    method: 'GET',
    headers: {
      'X-TBA-Auth-Key': global.TBA_AUTH_KEY
    }
  }
  const resp = await fetch(`https://www.thebluealliance.com/api/v3/${endpoint}`, config);
  const data = await resp.json();

  return data;
}

async function fetchEventKey(city) {
  const data = await fetchTBA('/events/2021/simple');
  const eventMatch = data.filter(event => event.city === city);
  
  if (eventMatch.length > 1) {
    console.error(`Conflict when getting event key, two or more events in ${city}.`);
    return;
  }
  else if (eventMatch == 0) {
    console.error(`Unable to find event in ${city}`);
    return;
  }
  // After the checks, there is only one event in the array

  return eventMatch[0].key;
}

async function loadMatchSchedule() {
  const eventKey = await fetchEventKey(global.CURRENT_EVENT_CITY);

  const allMatches = await fetchTBA(`/event/${eventKey}/matches/simple`);
  const qualificationMatches = allMatches
                                ?.filter(match => match.comp_level === "qm")
                                .sort((lhs, rhs) => lhs.match_number > rhs.match_number) || [];

  for (match of qualificationMatches) {
    const red = match.alliances.red;
    const blue = match.alliances.blue;

    const redWin = match.winning_alliance === "red";
    const blueWin = match.winning_alliance === "blue";

    const redColor = redWin ? "#fc9292" : "#ffcccb";
    const blueColor = blueWin ? "#7db5d4" : "#add8e6";

    const redClass = redWin ? "font-weight-bold" : "";
    const blueClass = blueWin ? "font-weight-bold" : "";

    $('#matchSchedule tbody').append(`
    <tr>
      <th scope="row">${match.match_number}</th>
      <td class="${redClass}" style="background-color: ${redColor};">${red.team_keys[0].substring(3)}</td>
      <td class="${redClass}" style="background-color: ${redColor};">${red.team_keys[1].substring(3)}</td>
      <td class="${redClass}" style="background-color: ${redColor};">${red.team_keys[2].substring(3)}</td>
      <td class="${blueClass}" style="background-color: ${blueColor};">${blue.team_keys[0].substring(3)}</td>
      <td class="${blueClass}" style="background-color: ${blueColor};">${blue.team_keys[1].substring(3)}</td>
      <td class="${blueClass}" style="background-color: ${blueColor};">${blue.team_keys[2].substring(3)}</td>
    </tr>
    `);
  }
}

async function loadRankings() {
  const eventKey = await fetchEventKey(global.CURRENT_EVENT_CITY);
  
  const data = await fetchTBA(`/event/${eventKey}/rankings`);
  console.log(data);
  const rankings = data.rankings?.map(team => [
    team.rank, // Current Rank
    team.team_key.substring(3), // Team number
    team.extra_stats[0] // Ranking Points
  ]) || [];
  console.log(rankings);
  
  return rankings;
}

$(document).ready(() => {
  $('#currentRankings').DataTable({
    paging: true,
    ordering: false,
    lengthChange: false,
    columnDefs: [{targets: 0, cellType: "th"}],
    info: false,
    language: {
      emptyTable: "No rankings data available. . ."
    },
    ajax: (data, callback, settings) => loadRankings().then(data => callback({ data: data }))
  })

  loadMatchSchedule()
    .then(_ => {
      // Initialize table after the match schedule is loaded
      $('#matchSchedule').DataTable({
        paging: true,
        ordering: false,
        lengthChange: false,
        language: {
          emptyTable: "No match data available. . ."
        }
      });
    });
  loadRankings();
});