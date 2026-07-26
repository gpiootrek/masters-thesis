/** Map of backend label → Polish display name and icon for the UI */
export const CATEGORY_META: Record<string, { name: string; icon: string }> = {
  'politics': { name: 'Polityka', icon: 'bank' },
  'economy, business and finance': { name: 'Gospodarka i Biznes', icon: 'chart' },
  'crime, law and justice': { name: 'Prawo i Sprawiedliwość', icon: 'gavel' },
  'environment': { name: 'Środowisko', icon: 'leaf' },
  'labour': { name: 'Praca', icon: 'briefcase' },
};

/**
 * Returns the display name for a given backend label.
 * Falls back to capitalizing the first letter if no mapping exists.
 */
export function getCategoryDisplayName(label: string): string {
  return CATEGORY_META[label]?.name ?? label.charAt(0).toUpperCase() + label.slice(1);
}

export function getCategoryIcon(label: string): string {
  return CATEGORY_META[label]?.icon ?? 'folder';
}
