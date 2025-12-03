"""Webhook service for event notifications."""

import logging
import httpx
from typing import Optional, Callable
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class WebhookEvent(str, Enum):
    """Types of webhook events."""

    QUERY_COMPLETED = "query.completed"
    ERROR_OCCURRED = "error.occurred"
    SESSION_CREATED = "session.created"
    SESSION_EXPIRED = "session.expired"
    RATE_LIMIT_EXCEEDED = "ratelimit.exceeded"


class WebhookService:
    """Service for managing webhooks and event notifications."""

    def __init__(self):
        """Initialize webhook service."""
        self.webhooks = {}
        self.events_log = []
        self.timeout = httpx.Timeout(10.0)

    def register_webhook(
        self,
        event_type: WebhookEvent,
        url: str,
        headers: Optional[dict] = None,
        active: bool = True,
    ) -> str:
        """
        Register a webhook endpoint.

        Args:
            event_type: Type of event to listen for
            url: Webhook URL
            headers: Optional custom headers
            active: Whether webhook is active

        Returns:
            Webhook ID
        """
        webhook_id = f"wh_{datetime.utcnow().timestamp()}"

        self.webhooks[webhook_id] = {
            "id": webhook_id,
            "event_type": event_type.value,
            "url": url,
            "headers": headers or {},
            "active": active,
            "created_at": datetime.utcnow(),
            "last_triggered": None,
            "trigger_count": 0,
        }

        logger.info(f"✓ Registered webhook: {webhook_id} for {event_type.value}")
        return webhook_id

    def unregister_webhook(self, webhook_id: str) -> bool:
        """Unregister a webhook."""
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"✓ Unregistered webhook: {webhook_id}")
            return True

        return False

    async def trigger_event(
        self,
        event_type: WebhookEvent,
        data: dict,
    ) -> int:
        """
        Trigger all webhooks for an event type.

        Args:
            event_type: Type of event
            data: Event data to send

        Returns:
            Number of successful webhooks
        """
        matching_webhooks = [
            w for w in self.webhooks.values()
            if w["event_type"] == event_type.value and w["active"]
        ]

        if not matching_webhooks:
            logger.debug(f"No webhooks registered for {event_type.value}")
            return 0

        success_count = 0
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for webhook in matching_webhooks:
                try:
                    payload = {
                        "event": event_type.value,
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": data,
                    }

                    response = await client.post(
                        webhook["url"],
                        json=payload,
                        headers=webhook["headers"],
                    )

                    if response.status_code >= 200 and response.status_code < 300:
                        webhook["last_triggered"] = datetime.utcnow()
                        webhook["trigger_count"] += 1
                        success_count += 1
                        logger.info(
                            f"✓ Webhook triggered: {webhook['id']} ({response.status_code})"
                        )
                    else:
                        logger.warning(
                            f"❌ Webhook failed: {webhook['id']} ({response.status_code})"
                        )

                except Exception as e:
                    logger.error(f"Webhook error: {webhook['id']} - {e}")

        # Log event
        self.events_log.append({
            "event": event_type.value,
            "timestamp": datetime.utcnow(),
            "webhook_count": len(matching_webhooks),
            "success_count": success_count,
        })

        return success_count

    def get_webhook(self, webhook_id: str) -> Optional[dict]:
        """Get webhook details."""
        return self.webhooks.get(webhook_id)

    def list_webhooks(
        self,
        event_type: Optional[WebhookEvent] = None,
        active_only: bool = False,
    ) -> list:
        """List webhooks with optional filtering."""
        webhooks = list(self.webhooks.values())

        if event_type:
            webhooks = [
                w for w in webhooks
                if w["event_type"] == event_type.value
            ]

        if active_only:
            webhooks = [w for w in webhooks if w["active"]]

        return webhooks

    def update_webhook(
        self,
        webhook_id: str,
        active: Optional[bool] = None,
        url: Optional[str] = None,
        headers: Optional[dict] = None,
    ) -> bool:
        """Update webhook configuration."""
        if webhook_id not in self.webhooks:
            return False

        webhook = self.webhooks[webhook_id]

        if active is not None:
            webhook["active"] = active

        if url is not None:
            webhook["url"] = url

        if headers is not None:
            webhook["headers"] = headers

        logger.info(f"✓ Updated webhook: {webhook_id}")
        return True

    def get_webhook_stats(self) -> dict:
        """Get webhook statistics."""
        total = len(self.webhooks)
        active = sum(1 for w in self.webhooks.values() if w["active"])
        total_triggered = sum(
            w["trigger_count"] for w in self.webhooks.values()
        )

        return {
            "total_webhooks": total,
            "active_webhooks": active,
            "total_triggered": total_triggered,
            "events_logged": len(self.events_log),
        }

    async def test_webhook(self, webhook_id: str) -> bool:
        """Test a webhook with a sample payload."""
        webhook = self.webhooks.get(webhook_id)
        if not webhook:
            return False

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    webhook["url"],
                    json={
                        "event": "webhook.test",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": {"test": True},
                    },
                    headers=webhook["headers"],
                )

                success = response.status_code >= 200 and response.status_code < 300
                logger.info(f"Webhook test: {webhook_id} - {'✓' if success else '❌'}")
                return success

        except Exception as e:
            logger.error(f"Webhook test error: {webhook_id} - {e}")
            return False


# Global instance
_webhook_service = None


def get_webhook_service() -> WebhookService:
    """Get or create webhook service instance."""
    global _webhook_service
    if _webhook_service is None:
        _webhook_service = WebhookService()
    return _webhook_service
