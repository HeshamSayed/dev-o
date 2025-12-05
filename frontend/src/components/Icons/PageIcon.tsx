import React from 'react';
import {
  Activity,
  AlarmClock,
  AlertCircle,
  AlertTriangle,
  ArrowRight,
  Bell,
  BookOpen,
  Bot,
  Brain,
  BriefcaseBusiness,
  Building2,
  CalendarDays,
  CircleCheckBig,
  ClipboardList,
  Cloud,
  Code2,
  Cog,
  Construction,
  Copy,
  Cpu,
  Database,
  Download,
  FileText,
  Gauge,
  Gift,
  GitBranch,
  Globe,
  Hammer,
  Hand,
  Handshake,
  Headphones,
  Image,
  Laptop,
  Layers,
  Library,
  Lightbulb,
  Link2,
  List,
  Lock,
  Mail,
  MapPin,
  MessageSquare,
  Mic,
  Microscope,
  Monitor,
  Network,
  NotebookPen,
  Package,
  Palette,
  Paperclip,
  PenTool,
  Puzzle,
  Rocket,
  Scale,
  Search,
  Send,
  Server,
  Share2,
  Shield,
  ShoppingBag,
  Shuffle,
  Star,
  Tag,
  Target,
  TrendingUp,
  Users,
  Waves,
  Webhook,
  Wrench,
  Zap
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

type IconComponent = LucideIcon;

export type PageIconName =
  | 'activity'
  | 'alert'
  | 'alertCircle'
  | 'arrow'
  | 'bell'
  | 'bolt'
  | 'book'
  | 'brain'
  | 'briefcase'
  | 'building'
  | 'calendar'
  | 'chart'
  | 'chat'
  | 'check'
  | 'clipboard'
  | 'cloud'
  | 'code'
  | 'construction'
  | 'copy'
  | 'cpu'
  | 'database'
  | 'dial'
  | 'download'
  | 'file'
  | 'gear'
  | 'gift'
  | 'git'
  | 'globe'
  | 'hammer'
  | 'hand'
  | 'handshake'
  | 'headphones'
  | 'image'
  | 'layers'
  | 'laptop'
  | 'library'
  | 'lightbulb'
  | 'link'
  | 'list'
  | 'lock'
  | 'mail'
  | 'map'
  | 'mic'
  | 'microscope'
  | 'monitor'
  | 'network'
  | 'note'
  | 'package'
  | 'palette'
  | 'paperclip'
  | 'pen'
  | 'puzzle'
  | 'robot'
  | 'rocket'
  | 'scale'
  | 'search'
  | 'send'
  | 'server'
  | 'share'
  | 'shield'
  | 'shopping'
  | 'shuffle'
  | 'star'
  | 'tag'
  | 'target'
  | 'users'
  | 'warning'
  | 'waves'
  | 'webhook'
  | 'wrench';

const iconMap: Record<PageIconName, IconComponent> = {
  activity: Activity,
  alert: AlarmClock,
  alertCircle: AlertCircle,
  arrow: ArrowRight,
  book: BookOpen,
  brain: Brain,
  briefcase: BriefcaseBusiness,
  building: Building2,
  calendar: CalendarDays,
  chat: MessageSquare,
  chart: TrendingUp,
  check: CircleCheckBig,
  clipboard: ClipboardList,
  cloud: Cloud,
  code: Code2,
  construction: Construction,
  copy: Copy,
  cpu: Cpu,
  database: Database,
  dial: Gauge,
  download: Download,
  file: FileText,
  gear: Cog,
  gift: Gift,
  git: GitBranch,
  globe: Globe,
  hand: Hand,
  handshake: Handshake,
  headphones: Headphones,
  image: Image,
  laptop: Laptop,
  layers: Layers,
  library: Library,
  lightbulb: Lightbulb,
  link: Link2,
  mail: Mail,
  map: MapPin,
  mic: Mic,
  microscope: Microscope,
  monitor: Monitor,
  network: Network,
  note: NotebookPen,
  package: Package,
  rocket: Rocket,
  shield: Shield,
  paperclip: Paperclip,
  pen: PenTool,
  puzzle: Puzzle,
  robot: Bot,
  star: Star,
  tag: Tag,
  users: Users,
  warning: AlertTriangle,
  wrench: Wrench,
  bolt: Zap,
  palette: Palette,
  shuffle: Shuffle,
  scale: Scale,
  search: Search,
  target: Target,
  hammer: Hammer,
  waves: Waves,
  list: List,
  lock: Lock,
  send: Send,
  server: Server,
  share: Share2,
  shopping: ShoppingBag,
  bell: Bell,
  webhook: Webhook
};

type PageIconProps = React.SVGProps<SVGSVGElement> & {
  name: PageIconName;
  size?: number;
  strokeWidth?: number;
};

export const PageIcon: React.FC<PageIconProps> = ({
  name,
  size = 24,
  className,
  strokeWidth = 1.75,
  ...props
}) => {
  const IconComponent = iconMap[name];

  if (!IconComponent) {
    return null;
  }

  return (
    <IconComponent
      className={className}
      size={size}
      strokeWidth={strokeWidth}
      {...props}
    />
  );
};
