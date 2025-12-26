from __future__ import annotations

import os
from pathlib import Path

from django.conf import settings
from django.core.files.base import File
from django.core.management.base import BaseCommand

from profiles.models import Profile


class Command(BaseCommand):
    help = (
        "Upload existing local Profile.avatar files to Cloudinary "
        "and update DB."
    )

    def handle(self, *args, **options):
        media_root = getattr(settings, "MEDIA_ROOT", None)

        if not media_root:
            self.stdout.write(self.style.ERROR("MEDIA_ROOT is not set."))
            self.stdout.write(
                "Temporarily set MEDIA_ROOT to your local media folder "
                "to migrate existing files."
            )
            return

        media_root_path = Path(media_root)

        migrated = 0
        skipped = 0
        missing = 0
        errors = 0

        qs = (
            Profile.objects.exclude(avatar="")
            .exclude(avatar__isnull=True)
        )

        for profile in qs:
            try:
                name = profile.avatar.name
                if not name:
                    skipped += 1
                    continue

                local_path = media_root_path / name
                if not local_path.exists():
                    missing += 1
                    continue

                with local_path.open("rb") as f:
                    profile.avatar.save(
                        os.path.basename(name),
                        File(f),
                        save=True,
                    )

                migrated += 1
            except Exception:
                errors += 1

        msg = (
            "Done. "
            f"migrated={migrated} "
            f"skipped={skipped} "
            f"missing={missing} "
            f"errors={errors}"
        )
        self.stdout.write(self.style.SUCCESS(msg))
