document.addEventListener('DOMContentLoaded', () => {
    const eventsList = document.getElementById('events-list');
    const shownEventIds = new Set();
    let firstLoad = true;

    function formatEventMessage(event) {
        if (event.type === 'PUSH') {
            return `${event.author} pushed to ${event.to_branch} on ${event.timestamp}`;
        } else if (event.type === 'PULL_REQUEST') {
            return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
        } else if (event.type === 'MERGE') {
            return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
        }
        return `Unknown event: ${JSON.stringify(event)}`;
    }

    function createEventCard(event) {
        const card = document.createElement('div');
        card.className = `event-card event-type-${event.type}`;
        
        const content = document.createElement('div');
        content.className = 'event-content';
        content.textContent = formatEventMessage(event);
        
        card.appendChild(content);
        return card;
    }

    async function fetchEvents() {
        try {
            const response = await fetch('/events');
            if (!response.ok) {
                console.error('Failed to fetch events');
                return;
            }
            const events = await response.json();
            
            // Remove "Waiting for events..." if we have data
            const loadingMsg = document.querySelector('.loading');
            if (events.length > 0 && loadingMsg) {
                loadingMsg.remove();
            }

            // Events come [Newest, ..., Oldest]
            // We want to add Newest to the TOP.
            // But we need to be careful not to re-add.
            // Iterate in reverse (Oldest -> Newest) is essentially verifying bottom up?
            // No, just iterate normally. If event is NOT in set, prepend it.
            // But if we iterate Newest(A) -> Oldest(B), and we prepend A, then B -> [B, A].
            // So we should iterate from Oldest to Newest (end of array to start).
            
            for (let i = events.length - 1; i >= 0; i--) {
                const event = events[i];
                if (!shownEventIds.has(event.request_id)) {
                    const card = createEventCard(event);
                    // Prepend to list (insert at beginning)
                    eventsList.insertBefore(card, eventsList.firstChild);
                    shownEventIds.add(event.request_id);
                }
            }

        } catch (error) {
            console.error('Error fetching events:', error);
        }
    }

    // Initial fetch
    fetchEvents();

    // Poll every 15 seconds
    setInterval(fetchEvents, 15000);
});
